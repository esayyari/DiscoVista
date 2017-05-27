#!/usr/bin/env python
import dendropy
import sys
import os
import copy
import os.path
from collections import Counter

HYPO = list(range(1,2))

lbls={}

def getLabel(taxon,hypo):
    t = lbls.get(taxon)
    if not t:
       raise Exception("%s not found in annotation file" %taxon)
    return t[hypo] 

def labeltree(tree, h):
    points = []
    for n in tree.postorder_node_iter():
        n.conflict = False
        if n.is_leaf():
            n.lbl=getLabel(n.taxon.label,h)
        else:
            nls = set (a.lbl for a in n.child_nodes())
            if len(nls) == 1: 
                n.lbl = nls.pop()
            else:
                n.lbl = "#".join(nls)
                #n.label = "#".join(nls)
                n.conflict = True
                points.extend((c for c in n.child_nodes() if not c.conflict))
    return points

def maptree(tree, h, map):
    for n in tree.postorder_node_iter():
        n.conflict = False
        if n.is_leaf():
            l = n.taxon.label
            cl = getLabel(l,h)
            map[cl] = map.get(cl,[]) + [l]


if __name__ == '__main__':

    if len(sys.argv) < 3: 
        print("USAGE: treefile annotationfile [collapse|contract]")
        sys.exit(1)

    treeName = sys.argv[1]
    annot = sys.argv[2]
    
    for x in open(annot):
        fields = x.strip().split('\t')
        lbls[fields[0]] = fields

    names = lbls['Code']

    trees = dendropy.TreeList.get_from_path(treeName, 'newick', preserve_underscores=True,rooting="default-rooted")

    if sys.argv[3] == "astral-mapping":
        for h in HYPO:
            map = dict()
            for t in trees:
                maptree(t,h,map)
            with open('map-astral-%d.txt' %h, 'w') as outfile:
                outfile.write("\n".join(
                                        ("%s:%s"%(k,",".join(v)) for k,v in map.items()))
                              )
        sys.exit(0)

    print(trees[0].is_rooted)
    
    if sys.argv[3] == "collapse":
        for i,t in enumerate(trees):
            h = HYPO[i]
            points = labeltree(t, h)
            for p in points:
                t = dendropy.Taxon(label=p.lbl)
                p.taxon = t
                for c in p.child_nodes():
                    p.remove_child(c)
        trees.write(file=open(treeName+"-collapsed.tre",'w'),schema='newick',suppress_rooting=True,unquoted_underscores=True)
        sys.exit(0)

        
    outrees = dendropy.TreeList()
    for i,t in enumerate(trees):
        for h in HYPO:
            tree = dendropy.Tree(t)
            #print(len(tree.seed_node.child_nodes()))
            print(names[h])

            points = labeltree(tree, h)
            counts = Counter((c.lbl for c in points))
            singles =  set(k for k,v in counts.items() if v == 1)
            print(singles)
            singleparents = list(x.parent_node for x in points if counts[x.lbl] == 1)
            print([k.lbl+ ":"+str(v) for k,v in Counter(singleparents).items()])
            root = list(k for k,v in Counter(singleparents).items() if v>1)[0]
            '''print counts
            for k,v in counts.iteritems():
                if (v == 1):
                    root = next(x for x in points if x.lbl == k)
                    break;'''
            #print ("root at parent of %s and current root is parent of %s and %s" %(str(root.lbl),c1,c2))
            tree.reroot_at_node(root)
            
            points = labeltree(tree, h)
            counts = Counter((c.lbl for c in points))
            print(counts)
            newroot = None
            for n in points:
                if n.lbl in set(["Out","Chromista"]):
                    newroot = n
                if n.is_leaf():
                    continue
                leaves = n.leaf_nodes()
                #print n.lbl, len(leaves)
                for child in n.child_nodes():
                   n.remove_child(child)
                for gc in leaves:
                   n.add_child(gc)
            if newroot:
                tree.reroot_at_edge(newroot.edge)
            print(len(tree.seed_node.child_nodes()))
            outrees.append(tree)    
            print()
    with open(treeName+"-hypo.tre",'w') as f:
        outrees.write(file=f,schema='newick',suppress_rooting=True,unquoted_underscores=True)
