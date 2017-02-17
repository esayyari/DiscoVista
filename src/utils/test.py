#!/usr/bin/env python
import glob
import re
import os
from tools import simplifyfasta

def occupancy(search):
    searchFiles = glob.glob(search)
    for fname in searchFiles:
        fname = os.path.abspath(fname)
        base = os.path.basename(fname)
        ID = os.path.basename(os.path.dirname(fname))
        splitBase = base.split("-")
        DS = splitBase[0]
        mode = ("-".join(splitBase[2:])).replace(".fasta","")

        output = simplifyfasta(fname)
        for line in output.split("\n"):
            if re.match(">", line) is not  None:
                taxon = re.sub(">","",line)
                continue
            else:
                newLine = re.sub("[N-]","",line)
                string = DS + " " + ID + " " + mode + " " + taxon + " " + str(len(newLine))
                print string

search = '../*/genes/*/*-alignment-noFilter.fasta'
occupancy(search)
