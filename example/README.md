# Structure of example data folder

## parameters

Under the __parameters__ folder, we have all the parameter files: 

* __annotation-1.txt__: Anootation file for the first hypothesis structure
* __annotation-2.txt__: Anootation file for the second hypothesis structure
* __annotation-3.txt__:  Anootation file for the third hypothesis structure
* __annotation-4.txt__: 	Anootation file for the forth hypothesis structure
* __annotation.txt__:	The overall anootation file. The main annotation file, where it maps every species available in your dataset (species tree) to a clade name. Note that you would assign each species to only one clade. 
* __clade-defs.txt__:    Clade definition file. In this file you would define all the clade definitions accourding to the instruction or the code provided previousely. Note that the field seperator in this file is tab. 
* __names.txt__:         Names file. List the names of the species you have in 
* __newModel.txt__:      Model condition definition file. In this file you would specify the old model condition names with exactly the ordering you want them get displayed on the x-axis of the species tree analysis on the first line. On the second line, you have the new naming for those model conditions with the same ordering. Note that the names are seperated with tabs instead of spaces.
* __newOrders.txt__:     Orders definition file. In this file you would specify the old clades names with exactly the ordering you want them get displayed on the first line, and the ordered new clades names on the second line of this file. Note that the names are seperated with tabs instead of spaces.
* __rooting.txt__:       Rooting definition file. In this rooting file you should specify the outgroup species, but you don't have to just list them in one line. You have this option to list them with respect to their distances to the ingroup species. For example, the rooting definition available here, has 3 lines, where on the first line we have the most distant species to the ingroups. On the other two lines we have the other outgroup species, with respect to their distance to the ingroup after the main set of outgroups.


## Species tree

Under the __species__ folder we have 31 folders each with this structure:
Model\_Condition-DST, where DST defines the type of sequence alignment. For example  __astral.trim50genes33taxa.no3rd.final-FNA2AA__ is a folder under the __species__ folder, where __astral.trim50genes33taxa.no3rd.final__ is the  model condition name, and __FNA2AA__ is the DST. Then under each folder we have a species tree with the name __estimated\_species\_tree.tree__.  In order to generate the same figures as available in the supplementary materials of the paper you would use the following commands if you installed __discoVista__ on your machine:

```bash
$WS_HOME/DiscoVista/src/utils/discoVista.py -c parameters/clade-defs.txt -p species/ -t 95 -y parameters/newModel.txt -w parameters/newOrders.txt -m 0 -o species/results
```

or using the docker image, you can run discovista with the following command. Note that __\<path to example folder\>__ is the absolute path to the directory where 1KP example folder is placed:

```bash
docker run  -v <path to example folder>/1KP:/data esayyari/discovista discoVista.py -c parameters/clade-defs.txt -p species/ -t 95 -y parameters/newModel.txt -w parameters/newOrders.txt -m 0 -o species/results
```

Here are the outputs:

![alt text][species-shade1]

[species-shade1]: figures/species/FNA2AA.block-shades.png ""

In this figure rows correspond to major orders and clades, and columns correspond to the results of different methods of the plant dataset. The spectrum of blue-green indicates amount of MLBS values for monophyletic clades. Weakly rejected clades correspond to clades that are not present in the tree, but are compatible if low support branches (below 90%) are contracted

![alt text][species]

[species]: figures/species/FNA2AA.block.png ""

In this figure rows correspond to major orders and clades, and columns correspond to the results of different methods ofthe plants dataset. Weakly rejected clades correspond to clades that are not present in the tree, but are compatible if low support branches (below 90%) are contracted.

## Genetrees

Under the __genetrees/filtered__ folder we have 852 folders each has 3 subfolders with one gene tree under each with the name __estimated\_gene\_trees.tree__. Each of these subfolders are named as __ID-Model\_Condition-DST__. More particularly, we have the __4032__ (ID) folder, and under this folder we have 3 subfolders __4032-c1c2_filterlen33-FNA2AA\_c1c2\_filterlen33__, __4032-filterlen33-FAA\_filterlen33__, and __4032-filterlen33-FNA2AA\_filterlen33__. In these folders __c1c2\_filterlen33__, and __filterlen33__ are the model conditions, and FAA and FNA2AA are the sequence alignment type.  In order to generate the same figures as available in the supplementary materials of the paper you would use the following commands if you installed __discoVista__ on your machine:

```bash
$WS_HOME/DiscoVista/src/utils/discoVista.py -c parameters/clade-defs.txt -p genetrees/filtered/  -t 75 -w parameters/newOrders.txt -y parameters/newModel.txt -m 1 -o genetrees/filtered/results
```

or using the docker image, you can run discovista with the following command. Note that __\<path to example folder\>__ is the absolute path to the directory where 1KP example folder is placed:

```bash
docker run -v <path to example folder>/1KP:/data esayyari/discovista discoVista.py -c parameters/clade-defs.txt -p genetrees/filtered/ -t 75 -w parameters/newOrders.txt -y parameters/newModel.txt -m 1 -o genetrees/filtered/results
```

Here are example outputs of this analysis:

![alt text][gt-portion]

[gt-portion]: figures/genetrees/Monophyletic_Bargraphs_Porportion.png ""


This figure shows the portion of RAxML genes for which important clades (x-axis) are highly (weakly) supported or rejected for three model conditions of the plants dataset. FAA-filterlen33: gene trees on amino acids sequences, and fragmentary sequences removed (66% gaps or more) FNA2AA-f25: amino acid sequences back translated to DNA, and sequences on long branches (25X median branch length)removed; FNA2AA-filterlen33: amino acid sequences back translated to DNA, and fragmentary sequences removed (66% gaps or more). Weakly rejected clades are those that are not in the tree but are compatible if low support branches (below 75%) are contracted.


![alt text][gt]

[gt]: figures/genetrees/Monophyletic_Bargraphs.png ""

This figure shows the number of RAxML genes for which important clades (x-axis) are highly (weakly) supported or rejected or are missing of three model conditions (same as above) of the plants dataset. Weakly rejected clades are those that are not in the tree but are compatible if low support branches (below 75%) are contracted.

## GC
We have the __GC/unfiltered__ folder available in the example folder. Under this folder we have 852 folders for each gene and the name of each folder is condsidered as the GENE ID, e.g. gene ID 4032. Then under each of these folders we have a __fasta__ file, with the name __DS-alignment-noFilter.fasta__. For example, __FNA2AA-alignment-noFilter.fasta__ is available under the folder __GC/unfiltered/4032__.  In order to generate the same figures as available in the supplementary materials of the paper you would use the following commands if you installed __discoVista__ on your machine:

```bash
$WS_HOME/DiscoVista/src/utils/discoVista.py -m 2 -p GC/unfiltered/ -o GC/unfiltered/results
```

or using the docker image, you can run discovista with the following command. Note that __\<path to example folder\>__ is the absolute path to the directory where 1KP example folder is placed:

```bash
docker run -v <path to example folder>/1KP:/data esayyari/discovista discoVista.py -m 2  -p GC/unfiltered/ -o GC/unfiltered/results
```

![alt text][gcpt]

[gcpt]: figures/GC/pTpP_GC_point.png ""


This figure corresponds to the GC content analysis of the 1kp dataset. Each dot shows the average GC content ratio for each species in all (red), first (pink), second (light blue), and third (dark blue) codon positions.

![alt text][gcbox]

[gcbox]: figures/GC/pTpP_GC_boxplot.png ""


This figure corresponds to the GC content analysis of the 1kp dataset, using boxplots for first, second, third, as well as all three codon positions.


## Occupancy
We have the __occupancy/filtered__ folder available in the example folder. Under this folder we have 852 folders for each gene and the name of each folder is condsidered as the GENE ID, e.g. gene ID 4032. Then under each of these folders we have a __fasta__ file, with the name __DST-alignment-Model\_Condition.fasta__. For example, __FNA2AA-alignment-f25.fasta__ and   __FNA2AA-alignment-filterlen33.fasta__ are available under the folder __occupancy/filtered/4032__.  In order to generate the same figures as available in the supplementary materials of the paper you would use the following commands if you installed __discoVista__ on your machine:

```bash
$WS_HOME/DiscoVista/src/utils/discoVista.py -m 3 -a parameters/annotation.txt -p occupancy/filtered/ -o occupancy/filtered/results
```

or using the docker image, you can run discovista with the following command. Note that __\<path to example folder\>__ is the absolute path to the directory where 1KP example folder is placed:

```bash
docker run -v <path to example folder>/1KP:/data esayyari/discovista discoVista.py -m 3 -a parameters/annotation.txt -p occupancy/filtered/ -o occupancy/filtered/results
```
Here are example outputs of this analysis:

![alt text][occ]

[occ]: figures/occupancy/occupancy.png ""

This figure shows the occupancy analysis on the 1kp dataset over each individual species for two model conditions (described above).



<p align="center">
<img src="figures/occupancy/occupancy_clades.png">
</p>


This figure shows the occupancy analysis on the important splits of 1kp dataset over each individual species for two model conditions (described above).


## Branch analysis
Under the folder __branchAnalysis__ available in the example folder, there are 6 folders, __GAMMA.2__, __c1c2.GAMMA.2__,  __c1c2.f25__,  __c1c2\_filterlen33__,  __f25__,  and   __filterlen33__, and under each of them we have a file with this naming structure __FNA2AA-estimated_gene_trees.tree__, where you would replace __FNA2AA__ with any alignment type or label that you wish, and each of them has 852 gene trees (lines) in the newick format.  In order to generate the same figures as available in the supplementary materials of the paper you would use the following commands if you installed __discoVista__ on your machine:

```bash
$WS_HOME/DiscoVista/src/utils/discoVista.py -m 4 -p branchAnalysis/ -r parameters/rooting.txt -o branchAnalysis/results
```

or using the docker image, you can run discovista with the following command. Note that __\<path to example folder\>__ is the absolute path to the directory where 1KP example folder is placed:

```bash
docker run  -v <path to example folder>/1KP:/data esayyari/discovista discoVista.py -m 4  -p branchAnalysis/ -r parameters/rooting.txt -o branchAnalysis/results
```



## Relative frequency 
Under the folder __relativeFreq/astral.trim50genes33taxa.no3rd.final-FNA2AA__, we have two files with the names __estimated\_species\_tree.tree__, and __estimated\_gene\_trees.tree__ for species tree, and set of gene trees (852) in newick format. In order to generate the same figures as available in the supplementary materials of the paper you would use the following commands if you installed __discoVista__ on your machine. Let's assume that you want to test the relative frequencies of the firts hypothesis (__annotation-1.txt__), in which there are 5 clades, _Base_ (as outgroup), _Charales_, _Coleochaetales_, _Landplants_, _Zygnematophyceae_. We use the following set of commands:

```bash
$WS_HOME/DiscoVista/src/utils/discoVista.py -a parameters/annotation-4.txt -m 5 -p relativeFreq/astral.trim50genes33taxa.no3rd.final-FNA2AA/ -o relativeFreq/astral.trim50genes33taxa.no3rd.final-FNA2AA/results/anot4 -g Base
```

or using the docker image, you can run discovista with the following command. Note that __\<path to example folder\>__ is the absolute path to the directory where 1KP example folder is placed:

```bash
docker run -v <path to example folder>/1KP:/data esayyari/discovista discoVista.py -a parameters/annotation-4.txt -m 5 -p relativeFreq/astral.trim50genes33taxa.no3rd.final-FNA2AA/ -o relativeFreq/astral.trim50genes33taxa.no3rd.final-FNA2AA/results/anot4 -g Base
```

Here is the example output of this analysis:

![alt text][relfreq]

[relfreq]: figures/relativeFreq/relativeFreq.png ""

This figure corresponds to the DiscoVista relative frequency analysis on 1kp dataset considering one hypothesis. Frequency of three topologies around focal internal branches of ASTRAL species trees using the trimmed gene trees (removing alignments with more than 66% gap characters) on first and second codon positions of amino acid alignments back translated to DNA in 1kp dataset. Main topologies are shown in red, and the other two alternative topologies are shown in blue. The dotted lines indicate the 1/3 threshold. The title of each subfigure indicates the label of the corresponding branch on the tree on the right (also generated by DiscoVista). Each internal branch has four neighboring branches which could be used to represent quartet topologies. On the x-axis the exact definition of each quartet topology is shown using the neighboring branch labels separated by “\#”.

