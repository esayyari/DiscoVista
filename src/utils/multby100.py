#!/usr/bin/env python


import dendropy
import sys

treefile = sys.argv[1]

trees = dendropy.TreeList.get(path=treefile,schema="newick")
outfile = sys.argv[2]
for tree in trees:
	for n in tree.internal_nodes():
            if n.label is not None:
                n.label = float(n.label) * 100.0
                n.edge.label = n.label

trees.write(file = open(outfile,'w'),schema='newick', suppress_rooting=True)



