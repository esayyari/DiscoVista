# Structure of example data folder

## parameters

Under the __parameters__ folder, we have all the parameter files: 

* __annotation-1.txt__: Anootation file for the first hypothesis structure
* __annotation-2.txt__: Anootation file for the second hypothesis structure
* __annotation-3.txt__:  Anootation file for the third hypothesis structure
* __annotation-4.txt__: 	Anootation file for the forth hypothesis structure
* __annotation.txt__:	The overall anootation file 
* __clade-defs.txt__:    Clade definition file
* __names.txt__:         Names file
* __newModel.txt__:      Model condition definition file
* __newOrders.txt__:     Orders definition file
* __rooting.txt__:       Rooting definition file


## Species

Under the __species__ folder we have 31 folders each with this structure:
Model\_Condition-DST, where DST defines the type of sequence alignment. For example  __astral.trim50genes33taxa.no3rd.final-FNA2AA__ is a folder under the __species__ folder, where __astral.trim50genes33taxa.no3rd.final__ is the  model condition name, and __FNA2AA__ is the DST. Then under each folder we have a species tree with the name __estimated\_species\_tree.tree__.

## Genetrees

Under the __genetrees/filtered__ folder we have 852 folders each has 3 subfolders with one gene tree under each with the name __estimated\_gene\_trees.tree__. Each of these subfolders are named as __ID-Model\_Condition-DST__. More particularly, we have the __4032__ (ID) folder, and under this folder we have 3 subfolders __4032-c1c2_filterlen33-FNA2AA\_c1c2\_filterlen33__, __4032-filterlen33-FAA\_filterlen33__, and __4032-filterlen33-FNA2AA\_filterlen33__. In these folders __c1c2\_filterlen33__, and __filterlen33__ are the model conditions, and FAA and FNA2AA are the sequence alignment type. 

## GC

## Occupancy

## Branch analysis

## Relative frequency 