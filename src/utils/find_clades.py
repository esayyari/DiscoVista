#!/usr/bin/env python
'''
Created on Jun 3, 2011

@author: smirarab
'''
import dendropy
import sys
import re
from types import ListType


def get_present_taxa(tree, labels):
    return [x.taxon for x in [tree.find_node_with_taxon_label(label) for label in labels]
            if x is not None]

class Mono(object):

    def __init__(self,taxa, outFile):
        self.allclades = dict()
        self.clades = dict()
        self.clade_comps = dict()
        self.alltaxa = taxa
        self.letters = dict()
        self.outFile = outFile
        self.show = dict()
    def print_result(self, treeName, keyword, mrca, lst, tree, ofile, mult):
        ln = "_".join([str(l) for l in lst]) if type(lst) == ListType else lst
        letter = self.letters[ln]
        name="%s (%s)" %(ln,letter) if letter is not None and letter!="" else ln
        support = "None"
        if mrca is not None and hasattr(mrca,'label'):
            if mrca.label is not None:
                support = str(float(mrca.label) * mult)
        elif hasattr(mrca,'label'):
            mrca.label = ""
        #mrca.label = "%s[%s]" %(ln,mrca.label) if mrca.label is not None else ln
        outputTree = treeName.replace(" ", "_") + ".out"
        #tree.write(path=outputTree, schema="newick", suppress_rooting=True)
        ofile.write("%s\t%s\t%s\t%s\n" % (treeName, keyword, support , name))

    def is_mono(self,tree, clade):
        mrca = tree.mrca(taxa=clade)
        for x in mrca.leaf_nodes():
            if x.taxon not in clade:
                return False, mrca
        return True, mrca
    def can_mono(self, tree, clade):
        mrca = tree.mrca(taxa=clade)
        for child in mrca.child_nodes():
            childLeaves = [x.taxon for x in child.leaf_iter()]
            intersect = [(x in clade) for x in childLeaves]
            # If a child of the mrca has both True and False (i.e. taxa of interest 
            # and others), it cannot be made monophyletic
            if (True in intersect) and (False in intersect):
                return False, mrca
            # If a child is all False (not taxa of interest), it is irrelevant.
            # If a child is all True (taxa of interst), it does not preclude monophyletic
        return True, mrca

    def check_mono(self,tree, treeName, clade, name, complete, ofile, mult):
        #print complete
        m, mrca = self.is_mono(tree, clade)
            #print m
        if m:
            if complete:
                self.print_result(treeName, "IS_MONO", mrca, name, tree, ofile, mult)
            else:
                self.print_result(treeName, "IS_MONO_INCOMPLETE", mrca, name, tree, ofile, mult)
            return
        c, mrca = self.can_mono(tree, clade)
        if c:        
            if complete:
                self.print_result(treeName, "CAN_MONO", mrca, name, tree, ofile, mult)
            else:
                self.print_result(treeName, "CAN_MONO_INCOMPLETE", mrca, name, tree, ofile, mult)
            return

        self.print_result(treeName, "NOT_MONO", mrca, name, tree, ofile, mult)

    def analyze_clade(self,name, clade, comps, tree, treeName, mult):
        ofile = open(self.outFile,'a+')
        taxa = get_present_taxa(tree, clade)
        taxaLabel = {t.label for t in taxa }
        if comps:
            for comp in comps:
                if not set(self.allclades[comp]) & taxaLabel:
                    self.print_result(treeName, "COMP_MISSING", None, name, tree, ofile, mult)
                    return
        if len(taxa) < 2:
            self.print_result(treeName, "NO_CLADE", None, name, tree, ofile, mult)
        else:
            self.check_mono(tree, treeName, taxa, name, len(taxa) == len(clade), ofile, mult)
        ofile.close()
    def analyze(self, tree, treeName, mult):
        for k, v in self.allclades.items():
            if self.show[k] == 1:
                if k in self.clade_comps:
                    clade_comp = self.clade_comps[k]
                else:
                    clade_comp = None
                self.analyze_clade(k, v, clade_comp, tree, treeName, mult)

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
		
                components=r[3].strip().split("+") if r[3] != "" and r[3] != "None" else []
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
        trees = dendropy.TreeList.get(path=fileName, schema='newick', rooting="force-rooted")
        labelsSet = set(t.label for t in trees.taxon_namespace)
        namemismatch = labelsSet - taxa
        if namemismatch:
            print >> sys.stderr, "The following taxa in the tree are not found in the names file:\n %s" %str(namemismatch)
            continue

        for i, tree in enumerate(trees):
            treeName = "%s_%s" % (fileName, i)
            mono.analyze(tree, treeName, 1.)


