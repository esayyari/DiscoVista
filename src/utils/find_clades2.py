#!/usr/bin/env python
import dendropy
import sys
import re
from types import ListType

#is_compatible_with_bipartition(bipartition, is_bipartitions_updated=False)
def get_present_taxa(tree, labels):
    return [x.taxon for x in [tree.find_node_with_taxon_label(label) for label in labels]
            if x is not None]
def get_support_from_bipartition(tree, clade, mult):
	bipartition = tree.taxon_namespace.taxa_bipartition(taxa=clade, is_mutable = False)
	clade2 = { c.taxon for c in tree.leaf_nodes() } - set(clade)
	
	bipartition2 = tree.taxon_namespace.taxa_bipartition(taxa=clade2, is_mutable = False)

	bipartition.is_mutable = False
	bipartition2.is_mutable = False

	clade = set(clade)
	
	e  = tree.bipartition_edge_map[bipartition]
	e2 = tree.bipartition_edge_map[bipartition2]
	if bipartition.is_trivial() or bipartition2.is_trivial():
                if float(mult) <  100:
                        return (1.0, e.length)
                else:
                        return(100.0, e.length)


	if e.label is None:
		#print e2, e2.label, e2.length, e.label, e.length
		return (e2.label,e2.length)
	else:
		return (e.label, e.length)
class Mono(object):

    def __init__(self,taxa, outFile):
        self.allclades = dict()
        self.clades = dict()
        self.clade_comps = dict()
	self.othercomps = dict()
        self.alltaxa = taxa
        self.letters = dict()
        self.outFile = outFile
        self.show = dict()
	self.c = 1
    def print_result(self, treeName, keyword, bipartition, lst, tree, ofile, mult, clade):
        ln = "_".join([str(l) for l in lst]) if type(lst) == ListType else lst
        letter = self.letters[ln]
        name="%s (%s)" %(ln,letter) if letter is not None and letter!="" else ln
	if keyword == "IS_MONO" or keyword == "IS_MONO_INCOMPLETE":
	        (support, length) = get_support_from_bipartition(tree, clade, mult)
		if support is None:
			print "WARNING some support was not available. Ignoring this branch",  " length was: ", length, "clade was: ", clade, "tree is: ",  tree
		support  = str(float(support) * float(mult))
	else:
		support = "None"
		length = "None"
        outputTree = treeName.replace(" ", "_") + ".out"
        #tree.write(path=outputTree, schema="newick", suppress_rooting=True)
        ofile.write("%s\t%s\t%s\t%s\t%s\n" % (treeName, keyword, support , name, length))
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
	#allTaxa = tree.leaf_nodes()
	#allTaxaLabels = {t.taxon.label for t in allTaxa}
        taxa = get_present_taxa(tree, clade)
	otherTaxaLabel = self.alltaxa - set(clade)
        taxaLabel = {t.label for t in taxa }
	otherSideTaxa = get_present_taxa(tree, otherTaxaLabel)
	othercomps = self.othercomps[name]
	otherTaxaLabel = {t.label for t in otherSideTaxa}
        if comps:
            for comp in comps:
                if not set(self.allclades[comp]) & taxaLabel:
                    self.print_result(treeName, "COMP_MISSING", None, name, tree, ofile, mult, clade)
                    return
	if othercomps and len(othercomps) != 0:
	    #print "othercomps", othercomps
	    for comp in othercomps:
		if comp != "":
			if not set(self.allclades[comp]) & otherTaxaLabel:
			    self.print_result(treeName, "COMP_MISSING", None, name, tree, ofile, mult, clade)
			    return	 
        #print len(taxa), len(clade)
        if len(taxa) < 2 or len(otherSideTaxa) < 2:
            self.print_result(treeName, "NO_CLADE", None, name, tree, ofile, mult, clade)
	    #if len(otherSideTaxa) < 2:
	    #	print tree.leaf_nodes(), taxa, taxaLabel, otherSideTaxa, otherTaxaLabel, tree
        else:
            self.check_mono(tree, treeName, taxa, name, len(taxa) == len(clade), ofile, mult, allBiparts)
        ofile.close()
    def analyze(self, tree, treeName, mult):
	for nd in tree.postorder_node_iter():
		nd.edge.label = nd.label
	tree_tmp = tree.clone(depth=1)
	allBiparts = [ t.compile_split_bitmask() for t in tree_tmp.encode_bipartitions(is_bipartitions_mutable = True) ]
	self.alltaxa = set(self.allclades["All"])
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
	    r[1] = r[1].strip()
	    r[0] = r[0].strip()
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

	    if len(r)>=6:
                othercomponents=r[5].strip().split("+") if r[5] != "" else []
            else:
                othercomponents=[]
            name = r[0]
            if len(r)>=4:
                self.letters[name] = r[2]
            else:
                self.letters[name] = ""
            self.allclades[name] = clade
            if r[3] != "None":
                self.clades[name] = clade
                self.clade_comps[name] = components
	    if len(r)>=6 and r[5] != "None":
		self.othercomps[name] = othercomponents
	    elif len(r)<6:
		self.othercomps[name] = othercomponents
            self.show[name] = show
def getTaxa(cladeFiles):
	
	f = open(cladeFiles, 'r')
	lines = f.readlines()
	flag = 0
	for line in lines:
		tmp = line.split('\t')[0]
		if (tmp == "All"):
			flag = 1
			line = line.strip('\n')
			listLine = line.split('\t')[1]
			taxa = set(listLine.replace('""+""','\t').replace('""','\t').replace('"','\t').replace('+','\t').strip('\t').replace('\t\t','\t').split('\t'))
	if flag == 0:
		print("Please define a clade with name All in your clade definition file, which includes all species in your dataset!")
		exit(1)
	return taxa
	f.close()

def main(*arg):
    namesFile = arg[0]
    cladesFile = arg[1]
    outFile = arg[2]
    mult = float(arg[3])

    taxa = getTaxa(cladesFile)
    #taxa = set(x.split('\t')[0].strip() for x in open(namesFile).readlines())
    #print taxa
    mono = Mono(taxa, outFile)
    mono.read_clades(cladesFile)
    
    for fileName in arg[4:][0].split(' '):
        trees = dendropy.TreeList.get(path=fileName, schema='newick', rooting="force-unrooted",preserve_underscores=True)
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
    taxa = getTaxa(cladesFile)
    #taxa = set(x.split('\t')[0].strip() for x in open(namesFile).readlines())	
    #print taxa
    mono = Mono(taxa, outFile)
    mono.read_clades(cladesFile)
    for fileName in sys.argv[4:]:
        trees = dendropy.TreeList.get(path=fileName, schema='newick', rooting="force-unrooted",preserve_underscores=True)
        labelsSet = set(t.label for t in trees.taxon_namespace)
        namemismatch = labelsSet - taxa
        if namemismatch:
            print >> sys.stderr, "The following taxa in the tree are not found in the names file:\n %s" %str(namemismatch)
            continue

        for i, tree in enumerate(trees):
            treeName = "%s_%s" % (fileName, i)
            mono.analyze(tree, treeName, 1.)


