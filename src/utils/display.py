#!/usr/bin/env python

import dendropy
import sys
import os
import re
import random

random.seed(a=885456)

def read_outgroup(outgroup_fp):
	with open(outgroup_fp) as f:
		a = f.readlines()[0]
		a = a.replace("\n","")
		return a.split("\t")

tree = dendropy.Tree.get(path=sys.argv[1],schema="newick",rooting="default-rooted",preserve_underscores=True)
if (len(sys.argv)>2):
	outgroup = " ".join(sys.argv[2:])
	print(outgroup)
	if os.path.exists(outgroup):
		outgroup_node =  tree.mrca(taxon_labels = read_outgroup(outgroup))
	else:
		allLeaves = {leaf.taxon.label for leaf in tree.leaf_nodes()}
		if outgroup not in allLeaves:
			print("Your outgroup species is not found! Please choose outgroup from these species: ", ", ".join(list(allLeaves)))
			sys.exit(1)
		outgroup_node = tree.find_node_with_taxon_label(outgroup)
else:
	outgroupNode = random.sample(tree.leaf_nodes(),1)[0]
	outgroup = outgroupNode.taxon.label
	outgroup_node = tree.find_node_with_taxon_label(outgroup)
new_root = tree.reroot_at_edge(outgroup_node.edge,suppress_unifurcations=True)
I = set()
Orig = set()
b=0
for nd in tree.postorder_internal_node_iter():
	b += 1
	if nd.label is not None and re.findall("N",nd.label):
		I.add(int(nd.label.replace("N","")))
		Orig.add(nd)
	

L = range(1, 2*len(tree.leaf_nodes()) )
O = list(set(L) - I)
c = 0
for nd in tree.preorder_node_iter():
	if  nd in Orig:
		nd.edge.length = int(nd.label.replace("N",""))
	else:	
		nd.edge.length = int(O[c])
		c += 1
children = new_root.child_nodes()
for c in children:
	if c == outgroup_node:
		tmplabel = c.edge.length
		other = list(set(children)-{c})
		break
other[0].edge.label =  tmplabel
other[0].edge.length = tmplabel
tree.write(path=sys.argv[1]+".out",schema= "newick",
        suppress_internal_taxon_labels=False,
        suppress_internal_node_labels=False,
        suppress_rooting=True,
        suppress_edge_lengths=False,
        unquoted_underscores=True,
        preserve_spaces=True,
        store_tree_weights=False,
        suppress_annotations=False,
        suppress_item_comments=False)
