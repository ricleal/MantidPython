'''
Created on Oct 29, 2015

@author: rhf
'''

import os
import logging, logging.config
import ConfigParser as configparser
import argparse

CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.cfg')
#LOCAL_CONFIG_FILE = os.path.expanduser('~/.convert_to_grasp.cfg')
LOCAL_CONFIG_FILE = os.path.join(os.path.abspath(os.path.curdir), 'metadata.cfg')

def get_parse_args():
    '''
    parse command line input arguments
    '''
    parser = argparse.ArgumentParser(description='Convert Mantid NeXus corrected to Grasp.')
    parser.add_argument('-i', '--infile', help='Mantid Corrected Nexus file to read the data', required=True)
    parser.add_argument('-o', '--outfile', help='Output file (data from the nexus file + metadata from the raw file)', required=True)
    parser.add_argument('-p', '--plot', help='Ploting options',  choices=['linear','log'], required=False)
    args = vars(parser.parse_args())
    return args

def get_config():
    '''
    Parse .cfg file
    '''
    config = configparser.ConfigParser()
    # config.optionxform=str # case insensitive
    config.read([CONFIG_FILE, LOCAL_CONFIG_FILE])
    return config

def get_logger():
    logging.config.fileConfig(CONFIG_FILE, disable_existing_loggers=False)
    logger = logging.getLogger()
    return logger
    

args = get_parse_args()
config = get_config()
logger = get_logger()