#!/bin/bash

tree=$1
method=$2
if [ "$method" == "avg" ]; then
	
	while read x; do 
		nw_distance -mm -sf -t <(echo $x) | tr "\t" "\n" | numlist -avg; 
	done < $tree
elif [ "$method" == "max" ]; then
	while read x; do
		nw_distance -mm -sf -t <(echo $x) | tr "\t" "\n" | numlist -max;
	done < $tree
fi
