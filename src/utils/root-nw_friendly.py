#!/usr/bin/env python
'''
Created on Jun 3, 2011

@author: smirarab
'''

import dendropy
import sys
import os
import copy
import os.path

hdir=os.path.dirname(os.path.realpath(__file__))
def readRoots(rootFile):
    f = open(rootFile,'r')
    ROOT = list()
    for line in f:
        line = line.replace("\n","")
        tmpRoot =  line.split(" ")
        ROOT.append(tmpRoot)
    return ROOT

#ROOTS = [
  #      ["IXODES_SCAPULARIS"],
 #       ["Symphylella_vulgaris","Glomeris_pustulata"],
   #     ["Lepeophtheirus_salmonis","DAPHNIA_PULEX"],["Cypridininae_sp","Sarsinebalia_urgorii","Celuca_puligator","Litopenaeus_vannamei"]]
        #["Anopheles_gambiae","Aedes_aegypti","Phlebotomus_papatasi","Tipula_maxima","Trichocera_fuscata","Bibio_marci","Bombylius_major","Drosophila_melanogaster","Lipara_lucens","Rhagoletis_pomonella","Glossina_morsitans","Sarcophaga_crassipalpis","Triarthria_setipennis"]]
def root (rootgroup, tree):
    root = None
    bigest = 0
    oldroot = tree.seed_node
    for n in tree.postorder_node_iter():
        if n.is_leaf():
            n.r = c.get(n.taxon.label) in rootgroup or n.taxon.label in rootgroup
            n.s = 1
        else:
            n.r = all((a.r for a in n.child_nodes()))
            n.s = sum((a.s for a in n.child_nodes()))
        if n.r and bigest < n.s:
            bigest = n.s
            root = n
    if root is None:
        return None
    #print "new root is: ", root.as_newick_string()
    newlen = root.edge.length/2 if root.edge.length else None
    tree.reroot_at_edge(root.edge,length1=newlen,length2=newlen,suppress_unifurcations=False)
    '''This is to fix internal node labels when treated as support values'''
    while oldroot.parent_node != tree.seed_node and oldroot.parent_node != None:
        oldroot.label = oldroot.parent_node.label
        oldroot = oldroot.parent_node
        if len(oldroot.sister_nodes()) > 0:
            oldroot.label = oldroot.sister_nodes()[0].label
    tree.suppress_unifurcations()
    return root

if __name__ == '__main__':

    if len(sys.argv) < 3: 
        print "USAGE: treefile root [output] "
        sys.exit(1)
    treeName = sys.argv[1]
    rooting = sys.argv[2]
    ROOTS = readRoots(rooting)
    if len(sys.argv ) == 4:
        resultsFile=sys.argv[3]
    else:
        resultsFile="%s.%s" % (treeName, "rerooted")
    
    c={}

    trees = dendropy.TreeList.get_from_path(treeName,'newick',rooting="force-rooted",preserve_underscores=True)
    for i,tree in enumerate(trees):
	roots = ROOTS
        while roots and root(roots[0],tree) is None:
	    roots = roots[1:]
        if not roots:
            print "Tree %d: none of the root groups %s exist. Leaving unrooted." %(i," or ".join((" and ".join(a) for a in ROOTS)))
    print "writing results to " + resultsFile        
    trees.write(path=resultsFile,schema='newick',suppress_rooting=True,suppress_leaf_node_labels=False)
