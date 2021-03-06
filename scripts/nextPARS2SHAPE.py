#!/usr/bin/python

import os
import glob
import argparse

# Convert nextPARS to SHAPE-like scores
# Usage: python nextPARS2SHAPE.py  --path $PATH_nextPARS_score_directory
# Files in directory must have .csv extension

parser = argparse.ArgumentParser(description='Convert nextPARS to SHAPE-like scores')


parser.add_argument('--path', help='PATH to nextPARS score directory')
parser.add_argument('--ext', nargs='?',const='.csv', help='File Extension')

args = parser.parse_args()


def linear_mapping(items):
	
	import numpy as np
	# multiplied by -1
	a = np.array(items)
	b = -a
	items = list(b)
	
	mx = max(items)
	mn = min(items)

	# Map 0s in tab to '-999' value
	# Linearly mapped to [0,1]
	res = list(map(lambda x: (x - mn)/(mx-mn) if x!=0 else -999, items))
	
	return res
	
path = args.path
 
ext = str(args.ext)

for filename in glob.glob(os.path.join(path, '*' + ext)):
	print (filename)
	name = os.path.basename(filename)
	outfile = path + '/' + name.replace(ext,".SHAPE")
	
	res = list()

	with open(filename, 'r') as f:
		for line in f:
			nline = line.rstrip().split(";")
			gene_name = nline[0]
			values = list(map(float,nline[1:-1]))
			k = 1
			for l in linear_mapping(values):
				res.append([k,l])
				k=k+1
		
		mfile = open(outfile,"w") 

		for number, letter in res:
			mfile.write("\n".join(["%s %s" % (number, letter)]) + "\n")


		
