#!/usr/bin/env python


import sys
import os
import re
from string import ascii_lowercase
import itertools

def iter_all_strings():
	size = 1
	while True:
		for s in itertools.product(ascii_lowercase, repeat = size):
			yield "".join(s)
		size += 1
		print size

gen = iter_all_strings()
def label_gen():
	for s in gen:
		return s

def expandname(filename):
	src_fpath = os.path.expanduser(os.path.expandvars(filename))
	if not os.path.exists(src_fpath):
		sys.stderr.write('Not found: "%s"' % src_fpath)
	return src_fpath

if __name__ == "__main__":


	annotate = expandname(sys.argv[1])
	listOfBipartitions = sys.argv[2]

	f = open(annotate,'r')
	anot = dict()
	allTaxa = set()
	for line in f:
		line = line.replace("\n","")
		line = line.split(" ")
		if line[1] in anot:
			anot[line[1]].append(line[0])
		else:
			anot[line[1]] = [line[0]]
		allTaxa.add(line[0])
	bipart = dict()
	for key in anot:
		anot[key] = sorted(anot[key])
		rest = sorted(list(allTaxa-set(anot[key])))
		if rest[0] < anot[key][0]:
			bipartition =  "/".join(rest)+"|"+"/".join(anot[key])
		else:
			bipartition = "/".join(anot[key])+"|"+"/".join(rest)
		bipart[bipartition] = key
	f.close()
	g = open(listOfBipartitions,'r')
	node = 0
	for line in g:
		line = "/".join(sorted(line.split(",")))
		
		if line in bipart:
			continue
		else:
			bipart[line] = label_gen()
			node = node + 1
	print len(bipart.keys())
	for key in bipart:
		bipart[key] = bipart[key].replace("\n","")
		keyt = key.replace("\n","")
		to_print = bipart[key] + " " + keyt 
		print to_print
