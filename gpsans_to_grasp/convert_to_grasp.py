#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Ricardo M. Ferraz Leal"

import sys
from pymantid import WorkSpace
from exporter import Exporter
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

    ws.info()
    exporter = Exporter(args['outfile'], ws)
    exporter.export()

if __name__ == "__main__":
    main(sys.argv)
    logger.info("Done!")
