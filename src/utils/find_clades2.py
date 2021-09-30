#!/usr/bin/env python
import dendropy
import sys
import re
import os
from types import ListType
def RepresentsInt(s):
    try: 
        float(s)
        return True
    except (TypeError, ValueError):
        return False

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
		if RepresentsInt(support) and RepresentsInt(mult):
			support  = str(float(support) * float(mult))
		else:
			support = "None"
			length = "None"
	else:
		support = "None"
		length = "None"
        outputTree = treeName.replace(" ", "_") + ".out"
        #tree.write(path=outputTree, schema="newick", suppress_rooting=True)
	try:
	        ofile.write("%s\t%s\t%s\t%s\t%s\n" % (treeName, keyword, support , name, length))
	except IOError:
		print("cannot write results on file for tree " + treename + " and clade " + name)
		sys.exit(1)
    def is_mono(self, tree, clade, allBiparts):
	try:
		taxon_namespace = tree.taxon_namespace 
		bipartition = taxon_namespace.taxa_bipartition(taxa=clade)
		bipartition = bipartition.compile_split_bitmask()
		allBiparts = set(allBiparts)
	except ValueError:
		cladeNames = [ t.label for t in clade ]
		print("some problem happened in checking monophyly of clade: " + " ".join(cladeNames))
		sys.exit(1)
	return (bipartition in allBiparts), bipartition
    def can_mono(self, tree, clade):
	try:	
		bipartition = tree.taxon_namespace.taxa_bipartition(taxa=clade)
		canMono = tree.is_compatible_with_bipartition(bipartition, is_bipartitions_updated=False)
	except ValueError:
		cladeNames = [ t.label for t in clade ]
		print("some problem happened in checking can-mono of clade: " + " ".join(cladeNames))
                sys.exit(1)
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
		if comp in self.allclades:
	                if not (set(self.allclades[comp]) & taxaLabel):
        	            self.print_result(treeName, "COMP_MISSING", None, name, tree, ofile, mult, clade)
                	    return
		else:
			print("clade comp is not defined previousely! please check your clade definition, 4th column for clade: " + name + " and component is: " + comp)
			sys.exit(1)
	if othercomps and len(othercomps) != 0:
	    #print "othercomps", othercomps
	    for comp in othercomps:
		if comp != "":
			if (not set(self.allclades[comp]) & otherTaxaLabel):
			    self.print_result(treeName, "COMP_MISSING", None, name, tree, ofile, mult, clade)
			    return
	    	else:
	    		print("clade comp is not defined previousely! please check your clade definition, 4th column for clade: " + name + " and component is: " + comp)
	    		sys.exit(1) 
        #print len(taxa), len(clade)
        if len(taxa) < 2 or len(otherSideTaxa) < 2:
            self.print_result(treeName, "NO_CLADE", None, name, tree, ofile, mult, clade)
	    #if len(otherSideTaxa) < 2:
	    #	print tree.leaf_nodes(), taxa, taxaLabel, otherSideTaxa, otherTaxaLabel, tree
        else:
	    try:
            	self.check_mono(tree, treeName, taxa, name, len(taxa) == len(clade), ofile, mult, allBiparts)
	    except ValueError:
	    	print("check mono failed for treeName: " + treeName + " taxa name: " + name )
	    	sys.exit(1)
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
	    if len(r)>1:
	    	r[1] = r[1].strip()
	    	r[0] = r[0].strip()
	    else:
	    	print("line: " + line + " in your clade def file is not tab seperated! please check your clade def file")
	    	sys.exit(1)
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
		if r[4].strip() == "":
			print("column 5 of clade definition file takes 0/1, but provided nothing! 0: don't show clade, 1: show the clade. Error occured in line: " + line)
			sys.exit(1)
		if RepresentsInt(r[4].strip()):
			if int(r[4].strip()) != 0 and int(r[4].strip())!= 1:
				print("column 5 of clade definition file takes 0/1! The number provided is " + r[4].strip() + " please check! Error occured in line: "+ line)
				sys.exit(1)
		else:
			print("column 5 of clade definition file takes 0/1, but provided a string instead! please check line: " + line)
			sys.exit(1)
                show = int(r[4].strip())
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
	try:	
		f = open(cladeFiles, 'r')
	except IOError:
		print("cannot open clade def file. Please check " + cladeFiles )
		sys.exit(1)
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
		sys.exit(1)
	return taxa
	f.close()

def main(*arg):
    namesFile = arg[0]
    cladesFile = arg[1]
    outFile = arg[2]
    if RepresentsInt(arg[3]):
    	mult = float(arg[3])
    else:
    	print("multiplier is not a number! " + mult)
	sys.exit(1)

    taxa = getTaxa(cladesFile)
    if taxa is None or len(taxa) == 0:
	print("Your clade 'All' has some problem! please check your clade definition file")
	sys.exit(1)
    #taxa = set(x.split('\t')[0].strip() for x in open(namesFile).readlines())
    #print taxa
    try:
    	mono = Mono(taxa, outFile)
    except ValueError:
	raise
    	print("Creating object Mono failed!")
    	sys.exit(1)
    try:
    	mono.read_clades(cladesFile)
    except ValueError:
	print("reading clade definition file failed")
	raise
    	sys.exit(1)

    fileNames = arg[4:][0].split(' ')
    
    errFlag = 0
    if len(fileNames) == 0:
	print("No tree files found! Please check!")
	sys.exit(1)
    else:
	print("Number of trees to analyze is: " + str(len(fileNames)))
    for fileName in arg[4:][0].split(' '):
	if not os.path.exists(fileName):
		print("tree file does not exist!")
		sys.exit(1)
	try:
	        trees = dendropy.TreeList.get(path=fileName, schema='newick', rooting="force-unrooted",preserve_underscores=True)
	except ValueError:
		raise
		print("cannot read tree file!")
     		sys.exit(1)
        labelsSet = set(t.label for t in trees.taxon_namespace)
        namemismatch = labelsSet - taxa
        if namemismatch:
	    errFlag = 1
            print >> sys.stderr, "The following taxa in the tree are not found in the names file:\n %s" %str(namemismatch)
            continue
	if errFlag == 1:
		print("some of the species in your tree are not found in the clade 'All'")
		sys.exit(1)
        for i, tree in enumerate(trees):
            treeName = "%s_%s" % (fileName, i)
	    try:
            	mono.analyze(tree, treeName, mult)
	    except ValueError:
		raise
	    	print("analyzing tree " + treeName + " failed!")
	    	sys.exit(1)
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


