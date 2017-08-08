#!/usr/bin/env python

import dendropy
import sys
import os
import re


tree = dendropy.Tree.get(path=sys.argv[1],schema="newick",rooting="forced_unrooted")

I = set()
Orig = set()
b=0
for nd in tree.postorder_node_iter():
	b += 1
	if nd.label is not None and re.findall("N",nd.label):
		I.add(int(nd.label.replace("N","")))
		Orig.add(nd)
	

L = range(1, 2*len(tree.leaf_nodes() -1)
O = list(set(L) - I)
c = 0
for nd in tree.preorder_node_iter():
	if  nd in Orig:
		nd.edge.length = int(nd.label.replace("N",""))
	else:	
		nd.edge.length = int(O[c])
		c += 1

tree.write(path=sys.argv[1]+".out",schema= "newick",
        suppress_internal_taxon_labels=False,
        suppress_internal_node_labels=False,
        suppress_rooting=True,
        suppress_edge_lengths=False,
        unquoted_underscores=False,
        preserve_spaces=False,
        store_tree_weights=False,
        suppress_annotations=False,
        suppress_item_comments=False)
