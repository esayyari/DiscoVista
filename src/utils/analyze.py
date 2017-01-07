import os
import glob
import re
import tools
import subprocess
import find_clades
import gc_stats
import tools
class Analyze(object): 
	def __init__(self,opt):
		self.opt = opt
	def gcStatAnalysis(self):
		opt = self.opt
		outFile = opt.path + "/gc-stat.csv"
		f = open(outFile, 'w')
		searchFile = " ".join(glob.glob(opt.search))
		for align in searchFile.split(" "):
			gc_stats.main(align)	
		print "All GC stat files have been generated"

		search = opt.path + "/*/gc-stat.txt"
	
		print >>f, "%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s" %("GENE","SEQUENCE","TAXON","A_C","C_C","G_C","T_C","N_C","frag_C","A_R","C_R","G_R","T_R","c1_A_C","c1_C_C","c1_G_C","c1_T_C","c1_N_C","c1_frag_C","c1_A_R","c1_C_R","c1_G_R","c1_T_R","c2_A_C","c2_C_C","c2_G_C","c2_T_C","c2_N_C","c2_frag_C","c2_A_R","c2_C_R","c2_G_R","c2_T_R","c3_A_C","c3_C_C","c3_G_C","c3_T_C","c3_N_C","c3_frag_C","c3_A_R","c3_C_R","c3_G_R","c3_T_R")	
		f.close()
		tools.concatenateFiles(outFile, search)	
		print "Concatenated GC stats are written to %s" % (outFile)
		currPath = os.path.dirname(os.path.abspath(__file__))
                WS_HOME = os.environ['WS_HOME']
                command = 'Rscript'
                path2script = WS_HOME  + "/DiscoVista/src/R/depict_clades.R"
                args = ["-p", WS_HOME, "-s", str(opt.mode), "-c", opt.clades, "-i", opt.path, "-a", opt.annotation]
                stderrFile = opt.path + "/error.log"
                cmd = [command, path2script] + args
                print "printing outputs and errors on " + stderrFile
                print cmd
		fi = open(stderrFile,'w')
                fi.close()
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = proc.communicate()
        #       x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
                err = open(stderrFile,'a')
                err.write(stdout)
                err.write(stderr)
                err.close()
	def occupancyAnalysis(self):
		opt = self.opt
		outFile = opt.path + "/occupancy.csv"
		tools.occupancy(opt.search, outFile)
		print "All the occupancy stats have written on file %s" % (outFile)  
		currPath = os.path.dirname(os.path.abspath(__file__))
                WS_HOME = os.environ['WS_HOME']
                command = 'Rscript'
                path2script = WS_HOME  + "/DiscoVista/src/R/depict_clades.R"
		if (opt.modelCond is None):
	                args = ["-p", WS_HOME, "-s", str(opt.mode), "-c", opt.clades, "-i", opt.path, "-a", opt.annotation]
		else:
			args = ["-p",  WS_HOME, "-s", str(opt.mode), "-c", opt.clades, "-i", opt.path, "-a", opt.annotation, "-x", opt.modelCond ]
                stderrFile = opt.path + "/error.log"
                cmd = [command, path2script] + args
                print "printing outputs and errors on " + stderrFile
                print cmd
		fi = open(stderrFile,'w')
		fi.close()
	
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = proc.communicate()
        #       x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
                err = open(stderrFile,'a')
                err.write(stdout)
                err.write(stderr)
                err.close()

	def treesAnalyses(self):
		opt = self.opt
		outFile = opt.path + "/clades.txt"
		f = open(outFile,'w')
		f.close()

		outFilethr = opt.path + "/clades.hs.txt"
		f = open(outFilethr,'w')
		f.close()
		finegrained = opt.path + "/finegrained"	
		if not os.path.exists(finegrained):
		    os.makedirs(finegrained)
		searchFiles = " ".join(glob.glob(opt.search))

		for tree in searchFiles.split(" "):
			tools.reroot(tree, opt.root, opt.annotation)
			tools.remove_edges_from_tree(tree, opt.threshold)
		
		searchFilesthr = " ".join(glob.glob(opt.searchthr))
		for tree in searchFilesthr.split(" "):
			tools.reroot(tree, opt.root, opt.annotation)

		searchFiles = " ".join(glob.glob(opt.searchrooted))
		searchFilesthr = " ".join(glob.glob(opt.searchthrrooted))
		if float(opt.threshold)<= 1.:
			multiplier = 100.
		else:
			multiplier = 1.
		find_clades.main(opt.names, opt.clades, outFile, multiplier, searchFiles) 
		find_clades.main(opt.names, opt.clades, outFilethr, multiplier, searchFilesthr)

		f = open(outFile,'r')
		outRes = outFile + ".res"

		oRes = open(outRes, 'w')
		outResthr = outFilethr + ".res"

		oResThr = open(outResthr, 'w')
		oRes.write("ID\tDS\tMONO\tBOOT\tCLADE\n")

		for line in f:
			linet = line.replace("\n","")
			listLine = linet.split("\t")
			b = os.path.basename(os.path.dirname(listLine[0]))

			#if opt.mode == 1:
			#	ID = os.path.basename(os.path.dirname(os.path.dirname(listLine[0])))
			#	method = re.sub("^-","",re.split(ID,b)[1])
			#else:
			ID = b
			tmp = re.split("-", b)
			method = tmp[len(tmp)-1]

			MONO = listLine[1]
			BOOT = listLine[2]
			CLADE = re.sub("\s+\(.*","", listLine[3])
			oRes.write( "%s\t%s\t%s\t%s\t%s\n" % (ID, method, MONO, BOOT, CLADE))
		f.close()
		oRes.close()
		oResThr.write("ID\tDS\tMONO\tBOOT\tCLADE\n")
		f = open(outFilethr,'r')
		for line in f:
			linet = line.replace("\n","")
			listLine = linet.split("\t")

			b = os.path.basename(os.path.dirname(listLine[0]))
		#	if opt.mode == 1:
		#		ID = os.path.basename(os.path.dirname(os.path.dirname(listLine[0])))
		#		method = re.sub("^-","",re.split(ID,b)[1])
		#	else:
			ID = b
			tmp = re.split("-", b)
			method = tmp[len(tmp)-1]

			MONO = listLine[1]
			BOOT = listLine[2]
			CLADE = re.sub("\s+\(.*","",listLine[3])
			oResThr.write( "%s\t%s\t%s\t%s\t%s\n" % (ID, method, MONO, BOOT, CLADE))
		oResThr.close()
		currPath = os.path.dirname(os.path.abspath(__file__))
		WS_HOME = os.environ['WS_HOME']
		command = 'Rscript'
		path2script = WS_HOME  + "/DiscoVista/src/R/depict_clades.R"
		args = ["-p", WS_HOME, "-s", str(opt.mode), "-c", opt.clades, "-i", opt.path, "-a", opt.annotation]
		stderrFile = opt.path + "/error.log"
		cmd = [command, path2script] + args
		print "printing outputs and errors on " + stderrFile
		print cmd
		fi = open(stderrFile,'w')
                fi.close()
		proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderr = proc.communicate()
	#	x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
		err = open(stderrFile,'a')
		err.write(stdout)
		err.write(stderr)
		err.close()
	def geneTreeBranchInfo(self):
		opt = self.opt
		searchFiles = " ".join(glob.glob(opt.search))
                for tree in searchFiles.split(" "):
                        tools.reroot(tree, opt.root, opt.annotation)
		treeName = glob.glob(opt.searchrooted)
		outFile = opt.path + "/branchStats.csv"
		outFile2 = opt.path + "/branchSupport.csv"
		tools.branchInfo(treeName, outFile, outFile2)	
		print "The branch Length and support values are written on file %s" % (outFile)
		currPath = os.path.dirname(os.path.abspath(__file__))
                WS_HOME = os.environ['WS_HOME']
                command = 'Rscript'
                path2script = WS_HOME  + "/DiscoVista/src/R/depict_clades.R"
                args = ["-p", WS_HOME, "-s", str(opt.mode), "-c", opt.clades, "-i", opt.path, "-a", opt.annotation]
                stderrFile = opt.path + "/error.log"
                cmd = [command, path2script] + args
                print "printing outputs and errors on " + stderrFile
                print cmd
		fi = open(stderrFile,'w')
                fi.close()
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = proc.communicate()
        #       x = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
                err = open(stderrFile,'a')
                err.write(stdout)
                err.write(stderr)
                err.close()
	def analyze(self):
		if self.opt.mode == 0 or self.opt.mode == 1:
			self.treesAnalyses()
		elif self.opt.mode == 2:
			self.gcStatAnalysis()
		elif self.opt.mode == 3:
			self.occupancyAnalysis()
		elif self.opt.mode == 4:
			self.geneTreeBranchInfo()
