#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Ricardo M. Ferraz Leal"

import sys
from pymantid import WorkSpace, Exporter
from settings import logger, args

"""
Convert corrected GPSANS file (NOT REDUCED!) in detector space to GRASP
"""


def main(argv):
    ws = WorkSpace(args['infile'])

    if args['plot'] == 'log':
        ws.plot2d_log()
    elif args['plot'] == 'linear':
        ws.plot2d()

    exporter = Exporter(args['outfile'])
    #exporter.as_config(ws)
    #exporter.as_json(ws)
    exporter.as_raw(ws)
    
if __name__ == "__main__":
    main(sys.argv)
    logger.info("Done!")
