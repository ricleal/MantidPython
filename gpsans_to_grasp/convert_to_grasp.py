#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Ricardo M. Ferraz Leal"

"""
Convert corrected GPSANS file (NOT REDUCED!) in detector space to GRASP
"""
import os
import logging, logging.config
import ConfigParser as configparser
import sys
import numpy as np
import argparse
from pprint import pprint, pformat

CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)),
'config.cfg')
config = configparser.ConfigParser()
config.optionxform=str # case insensitive
config.read([CONFIG_FILE, os.path.expanduser('~/.convert_to_grasp.cfg')])

logging.config.fileConfig(CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger()

sys.path.append(config.get('Mantid','path'))

def parse_args():
    '''
    parse command line input arguments
    '''
    parser = argparse.ArgumentParser(description='Convert Mantid NeXus corrected to Grasp.')
    parser.add_argument('-i', '--infile', help='Mantid Corrected Nexus file to read the data', required=True)
    parser.add_argument('-o', '--outfile', help='Output file (data from the nexus file + metadata from the raw file)', required=True)
    parser.add_argument('-p', '--plot', help='Ploting options',  choices=['linear','log'], required=False)
    args = vars(parser.parse_args())
    return args

def plot2d(data):
    logger.debug("Plotting 2D linear...")
    import matplotlib.pyplot as plt
    data = np.rot90(data,3)
    plt.imshow(data,
        aspect=0.5)
    plt.show()

def plot2d_log(data):
    logger.debug("Plotting 2D log...")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm
    data = np.rot90(data,3)
    plt.imshow(data,
        #cmap=plt.get_cmap("rainbow"),
        norm=LogNorm(vmin=np.min(data), vmax=np.max(data)),
        aspect=0.5)
    plt.show()

def get_metadata (mantid_ws):
    run = mantid_ws.getRun()
    return { k : run.getLogData(k).value for k in run.keys()}

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

def get_instrument_metadata (mantid_ws):
    instrument = mantid_ws.getInstrument()
    parameter_names = instrument.getParameterNames()
    return { parameter_names[i] : get_default_parameter(instrument,parameter_names[i])
            for i in range(parameter_names.size())}

def read_data_and_metadata(filename):
    '''
    Reads the mantid data into a numpy array
    Ignores the monitors
    Reshapes the data in 2D as the detector
    '''
    logger.info("Reading Mantid file: %s"%filename)
    import mantid.simpleapi as api
    detector_width = config.getint('Instrument','detector_width')
    detector_high = config.getint('Instrument','detector_high')
    try:
        ws = api.Load(filename)
    except Exception,e:
        logger.error("Cannot read Mantid file %s"%filename)
        logger.exception(e)
        sys.exit(-1)

    data = [ws.readY(i) for i in range(ws.getNumberHistograms()) if not ws.getDetector(i).isMonitor()]
    logger.debug("Data size = %d. Detector size = %d." % (len(data),detector_width*detector_high))
    data = np.array(data, dtype=np.int32)
    data = data.reshape([detector_width,detector_high])
    metadata = get_metadata (ws)
    metadata.update(get_instrument_metadata(ws))
    logger.debug("Data shape = %s." % str(data.shape))
    logger.debug(pformat(metadata))
    return data,metadata

def numpy_array_to_string(data):
    import io
    s = io.BytesIO()
    np.savetxt(s, data, delimiter='\t', fmt='%d')
    return s.getvalue()

def write_to_file(filename, metadata, data):
    '''
    '''
    logger.debug("Writting output to: %s."%filename)
    
    # Sort metadata by name
    from collections import OrderedDict
    metadata = OrderedDict(sorted(metadata.items(), key=lambda t: t[0]))

    with open(filename, 'w') as f:
        for k,v in metadata.items():
            f.write('%s=%s\n'%(k,v))
        f.write('\n')
        f.write(numpy_array_to_string(data))


def main(argv):
    args = parse_args()

    data,metadata = read_data_and_metadata(args['infile'])

    # # Set negative to 0 for plotting
    data_to_plot = data.clip(min=0.01)
    if args['plot'] == 'log':
        plot2d_log(data_to_plot)
    elif args['plot'] == 'linear':
        plot2d(data_to_plot)

    write_to_file(args['outfile'], metadata, data)

if __name__ == "__main__":
    main(sys.argv)
