#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Ricardo M. Ferraz Leal"

"""

Convert corrected GPSANS file (NOT REDUCED!) in detector space to GRASP

"""

MANTID_PATH = "/home/rhf/git/mantid/Build/bin"

FILENAME = '/home/rhf/git/MantidPython/gpsans_to_grasp/data/corrected_data.nxs'


#For the SANS detector, the (1,1) position is the bottom left corner as seen from the sample position. -->
DETECTOR_WIDTH = 192
DETECTOR_HIGH = 256

import sys
sys.path.append(MANTID_PATH)

import mantid.simpleapi as api
import numpy as np

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def plot2d(data):
    import matplotlib.pyplot as plt
    plt.imshow(data,
        aspect=0.5)
    plt.show()

def plot2d_log(data):
    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm
    plt.imshow(data,
        #cmap=plt.get_cmap("rainbow"),
        norm=LogNorm(vmin=np.min(data), vmax=np.max(data)),
        aspect=0.5)
    plt.show()

def read_data(filename = FILENAME):
    ws = api.Load(filename)

    # instrument = ws.getInstrument()
    # sample = ws.getInstrument().getSample()
    # source = ws.getInstrument().getSource()
    # samplePos = sample.getPos()

    # detector1 = instrument.getComponentByName('detector1')
    # print "Sample - Detector vector:", detector1.getPos()-sample.getPos()
    # print "Sample - Detector distance:", detector1.getDistance(sample)

    #data = np.empty([DETECTOR_WIDTH * DETECTOR_HIGH])

    data = [ws.readY(i) for i in range(ws.getNumberHistograms()) if not ws.getDetector(i).isMonitor()]
    print "Data size =", len(data), ". Detector size:", DETECTOR_WIDTH*DETECTOR_HIGH

    data = np.array(data, dtype=np.int32)
    #data = data.reshape([DETECTOR_HIGH,DETECTOR_WIDTH])
    #data = np.rot90(data,1)
    data = data.reshape([DETECTOR_HIGH,DETECTOR_WIDTH])
    data = np.rot90(data,2)

    print "Data shape =", data.shape
    return data

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
            print "ERROR:", k, "does not exist in the file", filename_in
    tree.write(filename_out)

def numpy_array_to_string(data):
    import io
    s = io.BytesIO()
    np.savetxt(s, data, delimiter='\t', fmt='%d')
    return s.getvalue()

def main(argv):
    data = read_data()

    # # Set negative to 0
    data_to_plot = data.clip(min=0.01)
    plot2d_log(data_to_plot)

    parse_xml('0001.xml', '0002.xml',
        {'Data/Detector': numpy_array_to_string(data) })


if __name__ == "__main__":
    main(sys.argv)
