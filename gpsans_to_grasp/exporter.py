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
from pprint import pformat
from abc import ABCMeta, abstractmethod
import importlib

sys.path.append(config.get('Mantid', 'path'))
import mantid.simpleapi as api

class Exporter(object):
    '''
    Mantid Workspace
    Simplified python version
    '''

    __metaclass__ = ABCMeta

    def __new__(cls, *arguments, **keywords):
        '''
        The class that will be created will be a subclass in the config file:
        General -> exporter
        '''
        for subclass in Exporter.__subclasses__():
            class_str = subclass.__module__ + "." + subclass.__name__
            if class_str == config.get('General','exporter'):
                return super(cls, subclass).__new__(subclass)
        raise Exception, 'Invalid Exporter! Use one of: %s'%([c.__name__ for c in Exporter.__subclasses__()])

    def __init__(self, filename, ws):
        if os.path.exists(filename):
            logger.warning("File %s exists and will be overwritten!"%filename)
        self.filename = filename
        self.ws = ws
        self.__init_data()

    @staticmethod
    def numpy_array_to_string(data):
        import io
        s = io.BytesIO()
        np.savetxt(s, data, delimiter='\t', fmt='%d')
        return s.getvalue()

    def __init_data(self):
        self.metadata = OrderedDict(sorted(self.ws.metadata.items(), key=lambda t: t[0]))
        self.instrument_metadata  = OrderedDict(sorted(self.ws.instrument_metadata.items(), key=lambda t: t[0]))
        self.user_metadata  = OrderedDict(sorted(config.items('Metadata'), key=lambda t: t[0]))
        self.data = Exporter.numpy_array_to_string(self.ws.data)

    @abstractmethod
    def export(self):
        pass


class Config(Exporter):
    def __init__(self, *args, **kwargs):
        logger.info("Exporting as Config")
        super(Config, self).__init__(*args, **kwargs)
    def export(self):
        '''
        '''
        logger.info("Writing output to: %s."%self.filename)
        with open(self.filename, 'w') as f:
            f.write('[Metadata]\n')
            for k,v in self.metadata.items():
                f.write('%s=%s\n'%(k,v))
            f.write('[InstrumentMetadata]\n')
            for k,v in self.instrument_metadata.items():
                f.write('%s=%s\n'%(k,v))
            f.write('[UserMetadata]\n')
            for k,v in self.user_metadata.items():
                f.write('%s=%s\n'%(k,v))
            f.write('\n')
            f.write(self.data)

class Raw(Exporter):
    def __init__(self, *args, **kwargs):
        logger.info("Exporting as Raw")
        super(Raw, self).__init__(*args, **kwargs)

    def _compile_data_in_a_single_dic(self):
        d = self.metadata.copy()
        d.update(self.instrument_metadata.copy())
        d.update(self.user_metadata.copy())
        OrderedDict(sorted(d.items(), key=lambda t: t[0]))
        return d

    def export(self):
        '''
        '''
        logger.info("Writing output to: %s."%self.filename)
        with open(self.filename, 'w') as f:
            for k,v in self._compile_data_in_a_single_dic().items():
                f.write('%s=%s\n'%(k,v))
            f.write('\n')
            f.write(self.data)

class Json(Exporter):
    def __init__(self, *args, **kwargs):
        logger.info("Exporting as Json")
        super(Json, self).__init__(*args, **kwargs)
    def export(self):
        '''
        '''
        logger.info("Writing output to: %s."%self.filename)
        data = {"metadata" :   self.metadata}
        data['instrument_metadata'] =   self.instrument_metadata
        data['user_metadata'] =   self.user_metadata
        data['data'] = self.data
        import json
        with open(self.filename, 'w') as f:
            json.dump(data, f)
