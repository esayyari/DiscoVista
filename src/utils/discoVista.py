#!/usr/bin/env python

import sys
import glob
import os
import re
from optparse import OptionParser
import find_clades 
import subprocess
from reader import Opt
from analyze import Analyze




if "__main__" == __name__:

    parser = OptionParser()

    parser.add_option("-a", "--annotation", dest="annotation",
                      help="The annotation file")

    parser.add_option("-c", "--clades", dest="clades",
                      help="The path to the clades definition file")


    parser.add_option("-m", "--mode", dest="mode",
                      help="Specifies the analysis to perform.\n To summarize species tree use 0. To summarize gene \ntrees use 1. For GC stat analysis use 2. For occupancy\n analysis use 3. For frequency analysis use 5.")

    parser.add_option("-p", "--path", dest="path",
                      help="path to the gene directory or species tree")

    parser.add_option("-r", "--rooting",dest="root",
                      help="The rooting file")

    parser.add_option("-s", "--style", dest="style",
                      help="The option file.", default = None)

    parser.add_option("-t", "--threshold", dest="thresh",
                      help="The bootstrap threshold")

    parser.add_option("-x", "--modelCond", dest="modelCond", default = None,
                      help="The model condition that the occupancy map will be plotted for")

    parser.add_option("-y", dest="newModel", default = None,
		      help="The new order for model conditions")

    parser.add_option("-w", dest="newOrder", default = None,
		      help="The new order for clades")

    parser.add_option("-k", "--missing", dest="missing", default = 0,
		      help="The missing data handling flag. If this flag set to one, clades with partially missing taxa are considered as complete.")
    
    parser.add_option("-o", "--output", dest="label", default = None,

		      help="name of the output folder for the relative frequency analysis. If you are using the docker it should start with '/data'.")
    parser.add_option("-g", "--outgroup", dest="outg", default = None,
		      help="Name of the outgroup for the hypothesis in relative frequency analysis specified in the annotation file, eg. Outgroup or Base.")

    parser.add_option("-f", "--figure", dest="figureFlag", default=0, type = int,
              help = "If user has previously run the code, and only wants to make figures again, should pass 1. Otherwise everything will be computed from the scratch." )
    opt = Opt(parser)

    analyzer = Analyze(opt)
    analyzer.analyze()

