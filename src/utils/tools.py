import glob
import os
import dendropy
import sys
import os.path
import re
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
def remove_edges_from_tree(*arg):

    treeName = arg[0]
    t = 75 if len(arg) < 2 else float(arg[1])
    if (t>1):
	t = int(t)
    resultsFile="%s.%s" % (treeName,t) if len(arg) < 4 or arg[3]=="-" else arg[2]
    #print "outputting to", resultsFile
    strip_internal=True if len(arg) > 4 and ( arg[3]=="-strip-internal" or arg[3]=="-strip-both" ) else False
    strip_bl=True if len(arg) > 4 and ( arg[3]=="-strip-bl" or arg[3]=="-strip-both" ) else False

    trees = dendropy.TreeList.get_from_path(treeName, 'newick')
    filt = lambda edge: False if (edge.label is None or (is_number(edge.label) and float(edge.label) >= t)) else True
    for tree in trees:
        for n in tree.internal_nodes():
            if n.label is not None:
                n.label = float (n.label)
                n.edge.label = n.label
                #print n.label
                #n.label = round(n.label/2)
        edges = set(tree.edges(filt))
        print >>sys.stderr, len(edges), "edges will be removed"
        for e in edges:
	    print e.label
            e.collapse()
        if strip_internal:
            for n in tree.internal_nodes():
                n.label = None
        if strip_bl:
            for e in tree.get_edge_set():
                e.length = None

        #tree.reroot_at_midpoint(update_splits=False)

    trees.write(file = open(resultsFile,'w'),schema='newick', suppress_rooting=True)

def concatenateFiles(outFile, search):
    searchFiles = " ".join(glob.glob(search))
    with open(outFile, 'a') as outfile:
        for fname in searchFiles.split(" "):
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

hdir=os.path.dirname(os.path.realpath(__file__))

def root (rootgroup, tree, c):
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

def readRoots(rootFile):
    f = open(rootFile,'r')
    ROOT = list()
    for line in f:
        line = line.replace("\n","")
        tmpRoot =  line.split(" ")
        ROOT.append(tmpRoot)
    return ROOT


def reroot(*arg):
    treeName = arg[0]
    rootDef =  arg[1]
    annotation = arg[2]
    if len(arg) == 4:
        resultsFile=arg[3]
    else:
        resultsFile="%s.%s" % (treeName, "rerooted")
    c={}
    for x in open(annotation):
        x.replace("\n","")
        c[x.split('\t')[0]] = x.split('\t')[1][0:-1]
    trees = dendropy.TreeList.get_from_path(treeName,'newick',rooting="force-rooted", preserve_underscores=True)
    ROOTS = readRoots(rootDef)
    for i,tree in enumerate(trees):
        roots = ROOTS
        while roots and root(roots[0],tree, c) is None:
            roots = roots[1:]
        if not roots:
            print "Tree %d: none of the root groups %s exist. Leaving unrooted." %(i," or ".join((" and ".join(a) for a in ROOTS)))
    print "writing results to " + resultsFile
    trees.write(path=resultsFile,schema='newick',suppress_rooting=True,suppress_leaf_node_labels=False, unquoted_underscores=True)
def branchSupports(tree, DS, model, g ):

    supp = list()
    for n in tree.postorder_node_iter():
        if n.is_leaf():
            continue
        elif (n.label is not None):            
            supp.append(float(n.label))
            string = DS + " " + model + " " + n.label + "\n"
            g.write(string)
    return supp


def simplifyfasta(filename):
    tmpfile = filename + ".tmp"
    g = open(tmpfile, 'w')
    f = open(filename, 'r')
    for line in f:
        line = line.rstrip('\n')
        r = re.sub('>(.*)', '@>\\1@', line)
        g.write(r)
    g.close()
    g = open(tmpfile, 'r')
    for line in g:
        line = re.sub('@','\n',line)
        line = re.sub('^\n','',line)
        return line
def occupancy(search, outFile): 
    searchFiles = glob.glob(search)
    g = open(outFile, 'w')
    for fname in searchFiles:
        fname = os.path.abspath(fname)
        base = os.path.basename(fname)
        ID = os.path.basename(os.path.dirname(fname))
        splitBase = base.split("-")
        DS = splitBase[0]
        mode = ("-".join(splitBase[2:])).replace(".fasta","")

        output = simplifyfasta(fname)
        for line in output.split("\n"):
            if re.match(">", line) is not  None:
                taxon = re.sub(">","",line)
                continue
            else:
                newLine = re.sub("[N-]","",line)
                string = DS + " " + ID + " " + mode + " " + taxon + " " + str(len(newLine))+"\n"
                g.write(string)
hdir=os.path.dirname(os.path.realpath(__file__))

def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n # in Python 2 use sum(data)/float(n)

def median(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('median requires at least one data point')
    return data[n/2] # in Python 2 use sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def pstdev(data):
    """Calculates the population standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/n # the population variance
    return pvar**0.5
def leafToLeafDistances(tree):
    pdm = tree.phylogenetic_distance_matrix()
    listTaxon = { n.taxon for n in tree.leaf_node_iter() }
    brLen = list()
    for idx1, taxon1 in enumerate(tree.taxon_namespace):
        if taxon1 not in listTaxon:
            continue
        for taxon2 in tree.taxon_namespace:
            if taxon2 not in listTaxon:
                continue
            mrca = pdm.mrca(taxon1, taxon2)
            weighted_patristic_distance = pdm.patristic_distance(taxon1, taxon2)
            brLen.append(weighted_patristic_distance)
    return brLen

def branchInfo(treeName, outFile, outFile2):
    c={}
    f = open(outFile, 'w')

    f.write("DS model_condition geneID medrootToLeafBrLen avgrootToLeafBrLen maxrootToLeafBrLen stdrootToLeafBrLen medtaxonToTaxonBrLen avgtaxonToTaxonBrLen maxtaxonToTaxonBrLen stdtaxonToTaxonBrLen medBrSupp avgBrSupp stdBrSupp\n")
    g = open(outFile2, 'w')
    for gene in treeName:
        r = os.path.basename(gene).split("-")
        mode = os.path.basename(os.path.dirname(gene))
        DS = r[0]
        trees = dendropy.TreeList.get_from_path(gene, 'newick',rooting="force-rooted", preserve_underscores=True)
        for i,tree in enumerate(trees):
            disrt = [n.distance_from_root() for n in tree.leaf_node_iter()]
            brLen = leafToLeafDistances(tree)
            supp = branchSupports(tree, DS, mode, g)			
            med = median(sorted(disrt))
            maxbrlen = max(disrt)
            avg = mean(disrt)
            std = pstdev(disrt)

            med2 = median(sorted(brLen))
            maxbrlen2 = max(brLen)
            avg2 = mean(brLen)
            std2 = pstdev(brLen)
            avgsupp = mean(supp)
            medsupp = median(sorted(supp))
            stdsupp = pstdev(supp)
            string = DS + " " + mode + " " + str(i+1) + " " + str(med) + " " + str(avg) + " " + str(maxbrlen) + " " + str(std) + " " + str(med2) + " " + \
                    str(avg2) + " " + str(maxbrlen2) + " " + str(std2) + " " + str(medsupp) + " " + str(avgsupp) + " " + str(stdsupp) + "\n"
            f.write(string)
    f.close()
    g.close()
