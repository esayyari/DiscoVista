#!/usr/bin/env python


import sys
import re
from find_clades2 import Mono

namesFile = sys.argv[1]
cladesFile = sys.argv[2]
freqStatFile = sys.argv[3]
outFile = sys.argv[4]
name = sys.argv[5]

g = open(outFile,'w')

taxa = set(x.split('\t')[0].strip() for x in open(namesFile).readlines())
mono = Mono(taxa, outFile)
mono.read_clades(cladesFile)
freqStat = open(freqStatFile).readlines()
clades = dict()
allOriginalClades = dict()
for clade in mono.allclades:
	key = ",".join(sorted(mono.allclades[clade]))
	clades[key] = clade
	key2 = ",".join(sorted(list(set(taxa) - set(mono.allclades[clade]))))
	clades[key2] = "Outside_"+clade
	
	allOriginalClades[clades[key2]]=list(set(taxa) - set(mono.allclades[clade]))
mono.allclades = dict(mono.allclades.items() + allOriginalClades.items())
tpTmp = list()
total = dict()
c=0
for line in freqStat:
		
	lineList = line.strip().strip("\n").split('\t')
	if lineList[1] == "t1":
		c = 0
		newLines = list()
	bipartitions = lineList[2].split("#")
	bipartquad1 = bipartitions[0].replace("}","").replace('|',"").split('{')[1:3]
	bipartquad2 = bipartitions[1].replace("}","").replace('|',"").split('{')[1:3] 
	topology1 = list()
	topology2 = list()
	quadT = list()
	for quad in bipartquad1:
		quadList = ",".join(sorted(quad.replace("_"," ").split(", ")))
		outsidequadList = ",".join(sorted(list(set(taxa)-set(quad.replace("_"," ").split(", ")))))
		if quadList in clades:
			topology1.append(clades[quadList])
		else:
			topology1.append(clades[outsidequadList])
		quadT = quadT + [x for x  in mono.allclades[clades[quadList]]]
	key1 = ",".join(sorted(quadT))
	key2 = ",".join(sorted(list(set(taxa)-set(quadT))))
	if lineList[1] == "t1":
		Node = clades[key1].replace("Outside_","")
	for quad in bipartquad2:
                quadList = ",".join(sorted(quad.replace("_"," ").split(", ")))
                topology2.append(clades[quadList])

	topology1 = sorted(topology1)
	key1 = ",".join(topology1)
	topology2 = sorted(topology2)
	key2 = ",".join(topology2)
	if topology1[0]<topology2[0]:
		string = key1+"|"+key2
	else:
		string = key2+"|"+key1
	finalLine = Node + "\t" + string + "\t" + "\t".join(lineList[2:6]) + "\t" + name
	newLines.append(finalLine)
	c = c + 1
	if c == 3:
		p0 = newLines[0] + "\t" + "t1"
		p1 = newLines[1]
		p2 = newLines[2]
		p1List = p1.split('\t')
		p2List = p2.split('\t')
		if p1List[1]<p2List[1]:
			p1 = p1 + "\t" + "t2"
			p2 = p2 + "\t" + "t3"
		else:
			p1 = p1 +"\t" + "t3"
			p2 = p2 + "\t" + "t2"

		print >> g, p0
		print >> g, p1
		print >> g, p2
		
