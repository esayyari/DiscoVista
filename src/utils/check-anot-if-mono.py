#!/usr/bin/env python

import os
import sys
import dendropy


def get_present_taxa(tree, labels):
    return [x.taxon for x in [tree.find_node_with_taxon_label(label) for label in labels]
            if x is not None]
def is_mono(tree, clades):
        tree_tmp = tree.clone(depth=1)
        allBiparts = [ t.compile_split_bitmask() for t in tree_tmp.encode_bipartitions(is_bipartitions_mutable = True) ]
	taxon_namespace = tree.taxon_namespace
	taxa = get_present_taxa(tree, clades)
        bipartition = taxon_namespace.taxa_bipartition(taxa=taxa)
        bipartition = bipartition.compile_split_bitmask()
        allBiparts = set(allBiparts)
        return (bipartition in allBiparts)


tree = dendropy.Tree.get_from_path(sys.argv[1], 'newick', preserve_underscores=True,rooting="default-rooted")

anot = (open(sys.argv[2],'r')).readlines()

clades = dict()

for line in anot:
	line = line.replace('\n','')
	line = line.strip('\n')
	line = line.strip()
	listLine = line.split('\t')
	if listLine[1] in clades:
		clades[listLine[1]].append(listLine[0])
	else:
		clades[listLine[1]] = list()
		clades[listLine[1]].append(listLine[0])

for clade in clades:
	m = is_mono(tree, set(clades[clade]))
	if m:
		continue
	else:
		print "The annotation file you've passed is not monophyletic for the clade " + str(clade).strip("\n") + ". Please check your annotation file."
		exit(1)

print "All clades specified in the annotation file are monophyletic"

