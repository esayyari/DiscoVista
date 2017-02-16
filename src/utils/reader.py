import sys
import os
from optparse import OptionParser
class Opt(object):
    def __init__(self, parser):
        (path, root, clades, threshold, mode, style, annotation, modelCond) = self.parseArgs(parser)
        tmpPath = os.path.dirname(annotation)
        self.names = tmpPath + "/names.txt"
        self.path = path
        self.root = root
        self.clades = clades
        self.threshold = threshold
        self.mode = mode
        self.style = style
        self.annotation = annotation
        self.modelCond = modelCond
        (search, searchthr, searchrooted, searchthrrooted) = self.searchFiles(mode, self.path, threshold)
        self.search = search
        self.searchthr = searchthr
        self.searchrooted = searchrooted
        self.searchthrrooted = searchthrrooted
        self.createNames(annotation, self.names)

    def parseArgs(self, parser):

        (options, args) = parser.parse_args()
        if not options.path:
            parser.print_help()
            sys.exit("please enter the path to the gene directory")

        path = options.path
        if not options.mode:
            parser.print_help()
            sys.exit("Please enter the mode. Do you want to summerize the species tree (0), or the gene trees (1)")

        mode = int(options.mode)
        if mode != 0 and mode != 1 and mode !=2 and mode != 3 and mode != 4:
            parser.print_help()
            sys.exit("To summerize species tree use 0, and to ummerize gene trees use 1. To do GC-stat analysis use 2. To do occupancy analysis use 3. To do branchInfo analysis please use 4.")
        if mode == 0 or mode == 1 or mode == 4:
            if not options.root:
                parser.print_help()
                sys.exit("Please enter the path to the rooting definitions")

            root = options.root
            root = os.path.abspath(root)

            if not os.path.isfile(root):
                parser.print_help()
                sys.exit("Please check the path to the rooting definitions")

        else:
            root = ""

        if mode == 0 or mode == 1:
            if not options.clades:
                parser.print_help()
                sys.exit("Please enter the path to clade definitions")

            clades = options.clades
            clades = os.path.abspath(clades)
            if not os.path.isfile(clades):
                parser.print_help()
                sys.exit("Please check the path to the rooting definitions")
    
            if not options.thresh:
                parser.print_help()
                sys.exit("Please enter the bootstrapping threshold")

            threshold = options.thresh

            if float(threshold)<=1.0:
                threshold = float(threshold)
            if not options.annotation:
                parser.print_help()
                sys.exit("Please enter the annotation file")

        else:
            clades = ""
            threshold = -1

        if not options.annotation:
            parser.print_help()
            sys.exit("Please enter the annotation file")    
        annotation = options.annotation
        annotation = os.path.abspath(annotation)
        if not os.path.isfile(annotation):
            parser.print_help()
            sys.exit("Please check the annotation file")

        path = os.path.expanduser(os.path.expandvars(path))
        path = os.path.abspath(path)
        if not os.path.exists(path):
            parser.print_help()
            sys.exit("please check the path to the gene direcotry")
        

        style = options.style
        modelCond = options.modelCond

        return (path, root, clades, threshold, mode, style, annotation, modelCond)
    def searchFiles(self, mode, path, thresh):
        if mode == 0:
            search = path + '/*/' + 'estimated_species_tree.tree'
            searchthr = path + '/*/' + 'estimated_species_tree.tree.' + str(thresh)
            searchrooted = path + '/*/' + 'estimated_species_tree.tree' + '.rerooted'
            searchthrrooted = path + '/*/' + 'estimated_species_tree.tree.' + str(thresh) + '.rerooted'
        elif mode == 1:
            search = path + '/*/*/' + 'estimated_gene_trees.tree'
            searchthr = path + '/*/*/' + 'estimated_gene_trees.tree.' + str(thresh)
            searchrooted = path + '/*/*/' + 'estimated_gene_trees.tree' + '.rerooted'
            searchthrrooted = path + '/*/*/' + 'estimated_gene_trees.tree.' + str(thresh) + '.rerooted'
        elif mode == 2:
            search = path + '/*/*-alignment-noFilter.fasta'
            searchthr = None
            searchrooted = None
            searchthrrooted = None
        elif mode == 3:
            search = path + '/*/*-alignment-*.fasta'
            searchthr = None
            searchrooted = None
            searchthrrooted = None
        elif mode == 4:
            search = path + '/*/*-estimated_gene_trees.tree'
            searchthr = None
            searchrooted = path + '/*/*-estimated_gene_trees.tree.rerooted'
            searchthrrooted = None
        return (search, searchthr, searchrooted, searchthrrooted)
    def createNames(self, annotation, names):
        f = open(names, 'w')
        g = open(annotation, 'r')
        for line in g:
            line = line.replace("\n","")
            r = line.split("\t")
            taxon = r[0].replace("_"," ")
            string = taxon + "\n"
            f.write(string)
        f.close()
            
    
