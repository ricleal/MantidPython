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

CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)),
'config.cfg')
config = configparser.ConfigParser()
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
    parser.add_argument('-t', '--templatefile', help='Instrument RAW data template file.', required=True)
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

def read_data(filename):
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
    #data = data.reshape([DETECTOR_HIGH,DETECTOR_WIDTH])
    #data = np.rot90(data,1)
    data = data.reshape([detector_width,detector_high])
    #data = np.rot90(data,2)

    logger.debug("Data shape = %s." % str(data.shape))
    return data

def prettify(elem):
    """
    Return a pretty-printed XML string for the Element.
    I also put's a new line after tag: <Detector type=(.*)>
    As GRASP does not read the data without this \n
    """
    from xml.etree import ElementTree
    from xml.dom import minidom
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_str = reparsed.toprettyxml(indent="  ", newl="", encoding="utf-8")
    # <Detector type="INT32[192,256]">
    import re
    pretty_str = re.sub(r'<Detector type=(.*)>',
       '<Detector type=\\1>\n',
        pretty_str)
    return pretty_str


def parse_xml(filename_in, filename_out, key_values_substitution):
    """
    Parses the XML file and will substitute
    key_values_substitution of format:
    {'SPICErack/Header/Sample_Name' : 'new sample name'}
    """
    from xml.etree import ElementTree as et
    tree = et.parse(filename_in)
    root = tree.getroot()
    for k,v in key_values_substitution.items():
        #tree.find('idinfo/timeperd/timeinfo/rngdates/begdate').text = '1/1/2011'
        tag = root.find(k)
        if tag is not None:
            tag.text = v
        else:
            logger.error("%s does not exist in the file %s." %(k,filename_in))
    pretty_xml = prettify(root)
    #tree.write(filename_out)
    logger.info("Writting data to %s...."%filename_out)
    with open(filename_out, "w") as text_file:
        text_file.write(pretty_xml)

def numpy_array_to_string(data):
    import io
    s = io.BytesIO()
    np.savetxt(s, data, delimiter='\t', fmt='%d')
    return s.getvalue()

def main(argv):
    args = parse_args()
    data = read_data(args['infile'])

    # # Set negative to 0
    data_to_plot = data.clip(min=0.01)
    if args['plot'] == 'log':
        plot2d_log(data_to_plot)
    elif args['plot'] == 'linear':
        plot2d(data_to_plot)

    parse_xml(args['templatefile'], args['outfile'],
        {'Data/Detector': numpy_array_to_string(data) })


if __name__ == "__main__":
    main(sys.argv)
