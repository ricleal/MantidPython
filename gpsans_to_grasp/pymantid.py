'''
Created on Oct 29, 2015

@author: rhf
'''

import sys
import os, os.path
from settings import args, config, logger
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from collections import OrderedDict

sys.path.append(config.get('Mantid','path'))
import mantid.simpleapi as api

class WorkSpace(object):
    '''
    Mantid Workspace
    Simplified python version
    '''
    def __init__(self, filename):
        '''
        Constructor
        '''
        
        # Inits
        self.data = None
        self.metadata = None
        self.instrument_metadata = None
        
        if not os.path.exists(filename):
            logger.error("File %s does not exist!")
            sys.exit(os.EX_OSFILE)
        self._parse_file(filename)
    
    def _parse_file(self,filename):
        logger.info("Reading Mantid file: %s"%filename)
        try:
            ws = api.Load(filename)
        except Exception,e:
            logger.error("Cannot read Mantid file %s"%filename)
            logger.exception(e)
            sys.exit(os.EX_IOERR)
        
        
        self.metadata = self._get_metadata(ws)
        self.instrument_metadata = self._get_instrument_metadata(ws)
        self.data = self._get_data(ws)
        api.DeleteWorkspace(ws)
        
    def _get_data(self,ws):
        detector_width = int(self.instrument_metadata['number-of-x-pixels'])
        detector_high = int(self.instrument_metadata['number-of-y-pixels'])
        data = [ws.readY(i) for i in range(ws.getNumberHistograms()) if not ws.getDetector(i).isMonitor()]
        logger.debug("Data size = %d. Detector size = %d." % (len(data),detector_width*detector_high))
        data = np.array(data, dtype=np.int32)
        data = data.reshape([detector_width,detector_high])
        return data
    
    def _get_instrument_metadata(self,ws):
        instrument = ws.getInstrument()
        parameter_names = instrument.getParameterNames()
        return { parameter_names[i] : WorkSpace.get_default_parameter(instrument,parameter_names[i])
                for i in range(parameter_names.size())}
        
    def _get_metadata(self,ws):
        run = ws.getRun()
        return { k : run.getLogData(k).value for k in run.keys()}
   
    def plot2d(self):
        logger.debug("Plotting 2D linear...")
        data = np.rot90(self.data,3)
        data = data.clip(min=0.01)
        plt.imshow(data,
            aspect=0.5)
        plt.show()
    
    def plot2d_log(self):
        logger.debug("Plotting 2D log...")
        data = np.rot90(self.data,3)
        data = data.clip(min=0.01)
        plt.imshow(data,
            #cmap=plt.get_cmap("rainbow"),
            norm=LogNorm(vmin=np.min(data), vmax=np.max(data)),
            aspect=0.5)
        plt.show()


    @staticmethod
    def get_default_parameter(instrument, name):
        """ Function gets the value of a default instrument parameter and
                assign proper(the one defined in IPF ) type to this parameter
                @param instrument --
            """
        if instrument is None:
            raise ValueError("Cannot initiate default parameter, instrument has not been properly defined.")
    
        type_name = instrument.getParameterType(name)
        if type_name == "double":
            val = instrument.getNumberParameter(name)
        elif type_name == "bool":
            val = instrument.getBoolParameter(name)
        elif type_name == "string":
            val = instrument.getStringParameter(name)
            if val[0] == "None" :
                return None
        elif type_name == "int" :
            val = instrument.getIntParameter(name)
        else :
            raise KeyError(" Instrument: {0} does not have parameter with name: {1}".format(instrument.getName(),name))
        return val[0]


class Exporter(object):
    '''
    Mantid Workspace
    Simplified python version
    '''
    def __init__(self, filename):
        if os.path.exists(filename):
            logger.warning("File %s exists and will be overwritten!"%filename)
        self.filename = filename
        
    @staticmethod
    def numpy_array_to_string(data):
        import io
        s = io.BytesIO()
        np.savetxt(s, data, delimiter='\t', fmt='%d')
        return s.getvalue()
    
    def as_config(self, ws):
        '''
        '''
        logger.info("Writing as_config output to: %s."%self.filename)
        # Sort metadata by name
        metadata = OrderedDict(sorted(ws.metadata.items(), key=lambda t: t[0]))
        instrument_metadata  = OrderedDict(sorted(ws.instrument_metadata.items(), key=lambda t: t[0]))
        
        with open(self.filename, 'w') as f:
            f.write('[Metadata]\n')
            for k,v in metadata.items():
                f.write('%s=%s\n'%(k,v))
            f.write('\n[InstrumentMetadata]\n')
            for k,v in instrument_metadata.items():
                f.write('%s=%s\n'%(k,v))
            f.write('\n[Data]\n')
            f.write(Exporter.numpy_array_to_string(ws.data))
    
    def as_raw(self, ws):
        '''
        '''
        logger.info("Writing as_raw output to: %s."%self.filename)
        
        instrument_metadata  = ws.instrument_metadata
        # metadata overwrites  instrument_metadata
        instrument_metadata.update(ws.metadata)
        # Sort
        instrument_metadata  = OrderedDict(sorted(ws.instrument_metadata.items(), key=lambda t: t[0]))
        
        with open(self.filename, 'w') as f:
            for k,v in instrument_metadata.items():
                f.write('%s=%s\n'%(k,v))
            f.write('\n')
            f.write(Exporter.numpy_array_to_string(ws.data))
            
    def as_json(self, ws):
        logger.info("Writing as_json output to: %s."%self.filename)
        data = {"metadata" :   ws.metadata}
        data['instrument_metadata'] =   ws.instrument_metadata
        data['data'] = ws.data.tolist()
        import json
        with open(self.filename, 'w') as f:
            json.dump(data, f)
    
        
    