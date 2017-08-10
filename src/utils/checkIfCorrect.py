#/usr/bin/env python
import sys
import glob
import re

alignDir = sys.argv[1]

mapping = sys.argv[2]

allAlignments = glob.glob(alignDir+'/*.fasta')

concatenatedAlignFile = alignDir + '/concatenated.phy'

concAlign = dict()

f = open(mapping,'r')

spInd=re.compile(">")
for g in f:
	alignment = g.split()[0]
	tmpf = open(alignDir + '/' + alignment + '.fasta','r')
	for line in tmpf:
		if re.search(">",line):
			sp = line.strip('\n').strip().split(">")[1]
		else:
			if sp in concAlign:
				string = concAlign[sp] + line.strip('\n').strip()
				concAlign[sp] = string
			else:
				concAlign[sp] = line.strip('\n').strip()
	tmpf.close()

sp = concAlign.keys()[0]
l = len(concAlign[sp])
print str(len(concAlign.keys())) + '  ' + str(l)
for key in concAlign:
	lt = len(concAlign[key])
	if lt != l:
		print "something is wrong " + str(l) + " " + str(lt) + ' ' + key + ' ' + sp
		exit(1)
	print key + ' ' + concAlign[key]
 
	 
