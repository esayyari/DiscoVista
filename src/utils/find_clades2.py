#!/usr/bin/env python
import dendropy
import sys
import re
from types import ListType

#is_compatible_with_bipartition(bipartition, is_bipartitions_updated=False)
def get_present_taxa(tree, labels):
    return [x.taxon for x in [tree.find_node_with_taxon_label(label) for label in labels]
            if x is not None]
def get_support_from_bipartition(tree, clade):
	bipartition = tree.taxon_namespace.taxa_bipartition(taxa=clade, is_mutable = False)
	bipartition.is_mutable = False
	clade = set(clade)
	e = tree.bipartition_edge_map[bipartition]
	return e.label
class Mono(object):

    def __init__(self,taxa, outFile):
        self.allclades = dict()
        self.clades = dict()
        self.clade_comps = dict()
        self.alltaxa = taxa
        self.letters = dict()
        self.outFile = outFile
        self.show = dict()
    def print_result(self, treeName, keyword, bipartition, lst, tree, ofile, mult, clade):
        ln = "_".join([str(l) for l in lst]) if type(lst) == ListType else lst
        letter = self.letters[ln]
        name="%s (%s)" %(ln,letter) if letter is not None and letter!="" else ln
	if keyword == "IS_MONO" or keyword == "IS_MONO_INCOMPLETE":
		
	        support = get_support_from_bipartition(tree, clade)
	else:
		support = "None"
        outputTree = treeName.replace(" ", "_") + ".out"
        #tree.write(path=outputTree, schema="newick", suppress_rooting=True)
        ofile.write("%s\t%s\t%s\t%s\n" % (treeName, keyword, support , name))
    def is_mono(self, tree, clade, allBiparts):
	taxon_namespace = tree.taxon_namespace 
	bipartition = taxon_namespace.taxa_bipartition(taxa=clade)
	bipartition = bipartition.compile_split_bitmask()
	allBiparts = set(allBiparts)
	return (bipartition in allBiparts), bipartition
    def can_mono(self, tree, clade):
	
	bipartition = tree.taxon_namespace.taxa_bipartition(taxa=clade)
	canMono = tree.is_compatible_with_bipartition(bipartition, is_bipartitions_updated=False)
        return canMono, bipartition

    def check_mono(self,tree, treeName, clade, name, complete, ofile, mult, allBiparts):
        #print complete
        m, bipartition = self.is_mono(tree, clade, allBiparts)
            #print m
        if m:
            if complete:
                self.print_result(treeName, "IS_MONO", bipartition, name, tree, ofile, mult, clade)
            else:
                self.print_result(treeName, "IS_MONO_INCOMPLETE", bipartition, name, tree, ofile, mult, clade)
            return
        c, bipartition = self.can_mono(tree, clade)
        if c and not m:        
            if complete:
                self.print_result(treeName, "CAN_MONO", bipartition, name, tree, ofile, mult, clade)
            else:
                self.print_result(treeName, "CAN_MONO_INCOMPLETE", bipartition, name, tree, ofile, mult, clade)
            return

        self.print_result(treeName, "NOT_MONO", bipartition, name, tree, ofile, mult, clade )

    def analyze_clade(self,name, clade, comps, tree, treeName, mult, allBiparts):
        ofile = open(self.outFile,'a+')
        taxa = get_present_taxa(tree, clade)
        taxaLabel = {t.label for t in taxa }
        if comps:
            for comp in comps:
                if not set(self.allclades[comp]) & taxaLabel:
                    self.print_result(treeName, "COMP_MISSING", None, name, tree, ofile, mult, clade)
                    return
        #print len(taxa), len(clade)
        if len(taxa) < 2:
            self.print_result(treeName, "NO_CLADE", None, name, tree, ofile, mult, clade)
        else:
            self.check_mono(tree, treeName, taxa, name, len(taxa) == len(clade), ofile, mult, allBiparts)
        ofile.close()
    def analyze(self, tree, treeName, mult):
	for nd in tree.postorder_node_iter():
		nd.edge.label = nd.label
	tree_tmp = tree.clone(depth=1)
	allBiparts = [ t.compile_split_bitmask() for t in tree_tmp.encode_bipartitions(is_bipartitions_mutable = True) ]
        for k, v in self.allclades.items():
            if self.show[k] == 1:
                if k in self.clade_comps:
                    clade_comp = self.clade_comps[k]
                else:
                    clade_comp = None
                self.analyze_clade(k, v, clade_comp, tree, treeName, mult, allBiparts)

    def read_clades(self,filename):
        for line in open(filename):
            line = line.replace("\n","")
            sign = "+"
            r = line.split('\t')
            if r[0] == 'Clade Name':
                continue
            clade = set()
            for x in re.split("([+|-])",r[1]):
                try:
                    if x in ["+","-"]:
                        sign = x
                    else:
                        x = x.strip("\"")
                        new = set(self.allclades[x] if x not in self.alltaxa else [x])
                        if sign == "+":
                            clade.update(new)
                        else:
                            clade.difference_update(new)
                except KeyError as e:
                    print "In %s, %s is not defined before" %(r[0],e.args[0])
                    sys.exit(1)
            clade = list(clade)

            if len(r)>=4:
                components=r[3].strip().split("+") if r[3] != "" else []
            else:
                components=[]
            if len(r)>=5:
                show = int(r[4].strip()) if r[4] != "" else 1
            else:
                show = 1

            name = r[0]
            if len(r)>=4:
                self.letters[name] = r[2]
            else:
                self.letters[name] = ""
            self.allclades[name] = clade
            if r[3] != "None":
                self.clades[name] = clade
                self.clade_comps[name] = components
            self.show[name] = show

def main(*arg):
    namesFile = arg[0]
    cladesFile = arg[1]
    outFile = arg[2]
    mult = float(arg[3])
    print mult
    taxa = set(x.split('\t')[0].strip() for x in open(namesFile).readlines())
    mono = Mono(taxa, outFile)
    mono.read_clades(cladesFile)
    for fileName in arg[4:][0].split(' '):
        trees = dendropy.TreeList.get(path=fileName, schema='newick', rooting="force-rooted")
        labelsSet = set(t.label for t in trees.taxon_namespace)
        namemismatch = labelsSet - taxa
        if namemismatch:
            print >> sys.stderr, "The following taxa in the tree are not found in the names file:\n %s" %str(namemismatch)
            continue

        for i, tree in enumerate(trees):
            treeName = "%s_%s" % (fileName, i)
            mono.analyze(tree, treeName, mult)

if __name__ == '__main__':
    namesFile = sys.argv[1]
    cladesFile = sys.argv[2]    
    outFile = sys.argv[3]
    taxa = set(x.split('\t')[0].strip() for x in open(namesFile).readlines())	
    mono = Mono(taxa, outFile)
    mono.read_clades(cladesFile)
    for fileName in sys.argv[4:]:
        print fileName    
        trees = dendropy.TreeList.get(path=fileName, schema='newick', rooting="force-unrooted")
        labelsSet = set(t.label for t in trees.taxon_namespace)
        namemismatch = labelsSet - taxa
        if namemismatch:
            print >> sys.stderr, "The following taxa in the tree are not found in the names file:\n %s" %str(namemismatch)
            continue

        for i, tree in enumerate(trees):
            treeName = "%s_%s" % (fileName, i)
            mono.analyze(tree, treeName, 1.)


