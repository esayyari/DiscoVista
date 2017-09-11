#!/usr/bin/env python

import sys
import os
import itertools
import string
def iter_all_strings():
    size = 1
    while True:
        for s in itertools.product(string.ascii_uppercase, repeat = size):
            yield "".join(s)
        size += 1
        print size

gen = iter_all_strings()
def label_gen():
    for s in gen:
        return s


if ("--help" in sys.argv) or ("-?" in sys.argv) or len(sys.argv) < 3 or ("-h" in sys.argv):
    sys.stderr.write("usage: %s [annotation file] [outputfile] [important branches file] \n" % sys.argv[0])
    sys.exit(1)

anotfile= os.path.abspath(sys.argv[1])
destfile = os.path.abspath(sys.argv[2])
if len(sys.argv) > 3:
    impBranch = os.path.abspath(sys.argv[3])
    if not os.path.exists(impBranch):
        sys.stderr.write('Not found: "%s"' % impBranch)
else:
    impBranch = None

if not os.path.exists(anotfile):
    sys.stderr.write('Not found: "%s"' % anotfile)
src = open(anotfile, "r")


print "Will write to file %s" % os.path.abspath(destfile)

clades = dict()
impClades = dict()
if impBranch is not None:
    with open(impBranch, 'r') as g:
        for line in g:
            label = label_gen()
            line = line.strip("\n")
            listTaxa = line.split("+")
            impClades[label] = listTaxa

for line in src:
    line = line.strip("\n")
    print line
    r = line.split("\t")
    taxa = r[0]
    clade = r[1]
    if clade not in clades:
        clades[clade] = list()
        clades[clade].append(taxa.replace("_"," "))
    else:
        clades[clade].append(taxa.replace("_"," "))
with open(destfile, 'w') as dest_file:
    dest_file.write("Clade Name\tClade Definition\tSection Letter\tComponents\tShow\tComments\n")
    allTaxa = set()
    for clade in clades:
        if clade != "Outgroup":
            taxa = clades[clade]
            tmp = {t for t in taxa}
            allTaxa = allTaxa | tmp
            if len(taxa)>1:
                string  = clade + "\t" + "\"" + taxa[0] + "+\"\"" + ("\"\"+\"\"").join(taxa[1:]) + "\"\"\"" + "\tNone\t\t1\t\n"
            else:
                string = clade + "\t" + "\"" + taxa[0] + "\"\"\"" + "\tNone\t\t0\t\n"

            dest_file.write(string)
        else:
            taxa = clades[clade]
            tmp = {t for t in taxa}
            allTaxa = allTaxa | tmp
            continue

    taxa = list(allTaxa)
    string = "All" + "\t" + "\"" + taxa[0] + "+\"\"" + ("\"\"+\"\"").join(taxa[1:]) + "\"\"\"" + "\tNone\t\t0\t\n"
    dest_file.write(string)
    if "Outgroup" in clades:
	    taxa = clades["Outgroup"] 
	    if len(taxa)>1:
        	string	= "Outgroup" + "\t" + "All" + "-\"" + taxa[0] + "-\"\"" + ("\"\"-\"\"").join(taxa[1:]) + "\"\"\"" + "\tNone\t\t1\t\n" 
	    else:
        	string = "Outgroup" + "\t" + "All" + "-\"" + taxa[0] + "\"\"\"" + "\tNone\t\t1\t\n"
	    dest_file.write(string)
    for clade in impClades:
        taxa = impClades[clade]
        if len(taxa)>1:
            string  = clade + "\t"  + taxa[0] + "+" + ("+").join(taxa[1:])  + "\tNone\t" +  taxa[0] + "+" + ("+").join(taxa[1:]) +   "\t1\t\n"
        else:
            string = clade + "\t"  + taxa[0]  + "\tNone\t\t0\t\n"

        dest_file.write(string)


