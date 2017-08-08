#!/usr/bin/env python
import sys
import dendropy


trees = dendropy.TreeList.get(path=sys.argv[1],schema="newick")


for tree in trees:
	tree.encode_bipartitions()
	for n in tree.postorder_node_iter():
		if n.is_leaf():
			continue
		if n.edge.bipartition.is_trivial():
			continue
		if n.label is not None:
			print n.label	
