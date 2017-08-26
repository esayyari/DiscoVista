# DiscoVista

DiscoVista (Discordance Visualization Tool) is a python and R-based software utility to analyze and visualize the phylogenetic information and gene discordances. 

## INSTALLATION:

### Installation using docker images:

Since DiscoVista has several dependencies and installation might be difficult and time consuming, we are now adding a docker image linked to the [DiscoVista github repository](https://github.com/smirarab/ASTRAL/tree/DiscoVista). Docker is a software container platform, which could be used to solve version control, compatibility and complex installation procedure problems. With docker, you should first install [docker](https://www.docker.com), and then pull the docker image from the dockerhub, and then you are ready to use DiscoVista. This is the procedure to use DiscoVista with docker:

* Install docker following the instractures for [Mac](https://docs.docker.com/docker-for-mac/install/), [Windows](https://docs.docker.com/docker-for-windows/install/), [Ubuntu](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/). If you have other operating systems please look at [here](https://www.docker.com/community-edition) for more details.  
* After installation and running the docker, you should pull docker with this command inside a terminal:

```bash
docker pull esayyari/discovista
```

This will pull the image.

* Then you can run DiscoVista following this command:

```bash
docker run -v <absolute path to data folder>:/data esayyari/discovista discoVista.py [OPTIONS]
```

By using "-v" we mount the data folder to /data folder inside the container, and all the changes and figures that DiscoVista creates will be available inside this folder. Also note that, __\<absolute path to data folder\>__ is an aboslute path, and program assumes that data is mounted under __/data__ inside container. We will talk about the proper set of options later. 

### Installation using source code:
The software package __DiscoVista__ depends on some R, and python packages. You could install __DiscoVista__ in a couple of steps:

Clone to [__DiscoVista__](https://github.com/esayyari/DiscoVista) git repository or download [this](https://github.com/esayyari/DiscoVista/archive/master.zip) zip file.
Then you need to set environmental variable __WS_HOME__ to the directory under which __DiscoVista__ repository is placed. For example, if you clone to DiscoVista and placed it under the __/Users/Erfan/reposiotry__ folder, then you would export __WS\_HOME__ as __/Users/Erfan/reposiotry__.


## R dependencies
DiscoVista uses R to do some postprocessing, and making figures. For more details regarding R and the installation instruction please see the following [link](https://www.r-project.org).
After installing R, there are some R packages that you need to install at this step. The R package dependencies are: __Reshape__, __Reshape2__, __ggplot2__, __plyr__, __scales__, __ape__, and __optparse__.

To install these packages you need to use the following command in R:

```R
install.packages(c("Reshape","Reshape2","ggplot2","plyr","scales","ape","optparse"))
```

## Python dependency
You need to install __DendroPy>=4.2.0__ as well. In Mac or Linux, you would use __pip__ to install DendroPy. If you have root access, you could use:

```bash
sudo pip install dendropy
```

otherwise, you would install dendropy with the command:

```bash
pip install dendropy --user
```

## Other dependencies
DiscoVista relies on two other softwares for performing its analyses as well. The first one is [newick utilities](http://cegg.unige.ch/newick_utils), and the other one is [ASTRAL-DiscoVista](https://github.com/smirarab/ASTRAL/tree/DiscoVista). Please install newick utilities, and add them to your __PATH__. Also, please put your ASTRAL folder under __WS\_HOME__, the same folder that DiscoVista lives. 

## Sample dataset

There is a sample dataset and the corresponding [result](https://github.com/esayyari/DiscoVista/tree/master/example) for each of the DiscoVista analyses. Also, there is a [README file](https://github.com/esayyari/DiscoVista/blob/master/example/README.md) which describes the data folder structure, the parameters, and exact commands used for each analysis. 

## How does DiscoVista work

The main utility to run these analyses is __discoVista.py__. To use this utility in bash you would use: 

```bash
Usage: discoVista.py [options]

Options:
  -h, --help            show this help message and exit
  -a ANNOTATION, --annotation=ANNOTATION
                        The annotation file
  -c CLADES, --clades=CLADES
                        The path to the clades definition file
  -m MODE, --mode=MODE  summerize gene trees or estimated species tree. To
                        summerize species tree use 0.  To summereize gene
                        trees use 1 . For GC stat analysis use 2.
  -p PATH, --path=PATH  path to the gene directory or species tree
  -r ROOT, --rooting=ROOT
                        The rooting file
  -s STYLE, --style=STYLE
                        The color style set
  -t THRESH, --threshold=THRESH
                        The bootstrap threshold
  -x MODELCOND, --modelCond=MODELCOND
                        The model condition that the occupancy map will be
                        plotted for
  -y NEWMODEL           The new order for model conditions
  -w NEWORDER           The new order for clades
  -k MISSING, --missing=MISSING
                        The missing data handling flag. If this flag set to
                        one, clades with partially missing taxa are considered
                        as complete.
  -o LABEL, --output=LABEL
                        name of the output folder for the relative frequency
                        analysis. If you are using the docker it should start
                        with '/data'.
  -g OUTG, --outgroup=OUTG
                        Name of the outgroup for the hypothesis in relative
                        frequency analysis specified in the annotation file,
                        eg. Outgroup or Base.
``` 

There are some files that you need to run these analyses. Note that some of these parameter files might not be needed for some of analyses. <a name="somefiles"></a>

1. You would pass the annotation file to the utility using **-a ANNOTATION**. In each line of this file, you need the taxon name and the corresponding clade name that species belongs to. Please use tab as the separator. 
2. You would pass the rooting definition file to the utility using **-r ROOT**. Let's say that you have an **outgroup** clade. On the lines of this file, the set of species in the order of speciation events time are listed. The set of species on the first line belongs to the species that are the most distant species to the ingroup species. The next line belongs species in the outgroup which are the second most distant species to the ingroup species, and so on. 
3. You would pass the clade definition file to the utility using **-c CLADE**. There is an example of this file available under the DiscoVista GitHub repository. Also, there is another tool to generate this clade definition file in this repository under DiscoVista/src/utils/generate_clade-defs.py. 

### How to generate clade definition file
Clade definition file has different columns. The column names are: __Clade Name__, __Clade Definition__, __Section Letter__ , __Components__,    __Show__, and    __Comments__.

* __Clade Name__ defines the name of clade
* __Clade Definition__ is the list of species or other clades in this clade. You would use **+** or **-** signs to define them.
* __Section Letter__ Name that will define the order of clades. If there is no ordering between clades leave it blank. 
* __Components__ The list of important species or clades that defines the clade. If one of these species or clades is missed, the clade will be considered as missing.
* __Show__ This is a 0/1 variable. If this is 1, that clade will be considered for the analyses, otherwise, this clade will not be considered for analysis. 
* __Comments__ comments about the clade.

Also, there is the python code **generate_clade-defs.py** that could be used to generate the clade definition file from the annotation file. You would use it using the command:

```bash
generate_clade-defs.py [annotation file] [outputfile] [important branches file]
```

In important branches file, you could define other important branches of the expected tree. Let's say that we have two clades **A**, and **B**, and you are interested in the branch that separates **AB** from others. Then you would define it with **A+B** in this file.

## How to use DiscoVista
Throughout this tutorial, we assume that you are using bash, and your current directory is **WS\_HOME/DiscoVista/**. The rooting definitions are listed in rooting.txt under **WS\_HOME/DiscoVista/parameter**, the annotation file is annotation.txt under **WS\_HOME/DiscoVista/parameter**, and the clade definition file is clade-definition.txt under **WS\_HOME/DiscoVista/parameter** folder (as described [above](#somefiles)). Also,  I assume that the output will be written under __\<the analysis folder>/results__ folder.

### 1. Discordance analysis on species trees
To perform discordance analysis on species trees, you need gene trees with the MLBS values  [local posterior probabilities] (https://github.com/smirarab/ASTRAL) draw on the branches and represented in Newick format as node labels. For drawing MLBS on branches we highly recommend using [newick utilities](http://cegg.unige.ch/newick_utils). Please double check the support values after rerooting with our tool using any graphical viewing software like [FigTree](http://tree.bio.ed.ac.uk/software/figtree/) to be sure support values are correctly drawn and rerooting was correct. 
 

* Species trees should be stored following this structure **path/MODEL\_CONDITION-DST/estimated\_species\_tree.tree**. Here __path__ points to the directory that species trees are located. Put each estimated species tree inferred with different methods under different directories. The name of these directories should follow **model\_condition-data\_sequence\_type**. For example, if you have different filtering strategies for your nucleotide acid sequences and then the gene trees are inferred using [RAxML](http://sco.h-its.org/exelixis/web/software/raxml/index.html), you might put the species tree with name estimated\_species\_tree.tree, under RAxML\_highly\_filtered-NA.  Please only use **"-"** to separate the model condition from the data sequence type.

* Let's assume that the MLBS values are drawn on branches of the species tree available at path **\<path\>**, and there are 3 model conditions, RAxML\_highly\_filtered-NA, RAxML\_med\_filtered-NA, and RAxML\_highly\_filtered-NA. Also, assume that you consider branches with MLBS above 95 as highly supported branches, and the code will contract branches below that. Then you would call the software in bash using the following command:

```bash
./discoVista.py -m 0 -c clades-def.txt -p $path -t 95 -o $path/results 
```


* Using docker:

```bash
docker run -v <absolute path to data folder>:/data esayyari/discovista discoVista.py discoVista.py -m 0 -c clades-def.txt -p $path -t 95 -o $path/results 
```


* If you are using local posterior probabilities instead of MLBS, and let's assume that the branches above the threshold of 0.95 considered as highly supported branches, then you would use the software with:

```bash
./discoVista.py -m 0  -c parameter/clades-def.txt -p $path  -t 0.95 -o $path/results 
```

*  Using docker:

```bash
docker run -v <absolute path to data folder>:/data esayyari/discovista discoVista.py -m 0 -c /data/parameter/clades-def.txt -p $path  -t 0.95 -o $path/results 
```


Here are the example outputs of the:

![alt text][species-shade]

[species-shade]: example/figures/species/FNA2AA.block-shades.png ""

In this figure rows correspond to major orders and clades, and columns correspond to the results of different methods of  previously published dataset of plants (Wickett, et al., 2014, PNAS). The spectrum of blue-green indicates amount of MLBS values for monophyletic clades. Note that we have the results of one species tree with Bayesian support values instead of MLBS values, and the support values are not directly comparable. Weakly rejected clades correspond to clades that are not present in the tree, but are compatible if low support branches (below 90%) are contracted

![alt text][species]

[species]: example/figures/species/FNA2AA.block.png ""

In this figure rows correspond to major orders and clades, and columns correspond to the results of different methods of  previously published dataset of plants (Wickett, et al., 2014, PNAS). Weakly rejected clades correspond to clades that are not present in the tree, but are compatible if low support branches (below 90%) are contracted.


### 2. Discordance analysis on gene trees

To perform discordance analysis on gene trees, you need gene trees with the MLBS values draw on the branches and represented in Newick format as node labels. For drawing MLBS on branches we highly recommend using [newick utilities](http://cegg.unige.ch/newick_utils). 

* Gene trees should be stored using this structure **path/GENE\_ID/GENE\_ID-MODEL\_CONDITION-DST/estimated\_gene\_trees.tree**. Here __path__ points to the directory that gene trees are located. Please only use **"-"** to separate the gene ID, model condition, and data sequence type. Put each estimated gene tree inferred with different methods for the different gene under different directories. The name of these directories should follow **GENE\_ID-model\_condition-data\_sequence\_type**. 

* Note that you should do this analysis for each model condition separately. 

* Let's assume that the MLBS values are drawn on branches of the gene trees of model condition RAxML\_highly\_filtered-NA available at path **path**. Also, assume that you consider branches with MLBS above 75 as highly supported branches, and the code will contract branches below that. Then you would call the software in bash using the following command:

```bash
./discoVista.py -m 1 -c parameter/clades-def.txt -p $path -t 75 -o $path/results 
```

* Using docker:

```bash
docker run -v <absolute path to data folder>:/data esayyari/discovista discoVista.py -m 1 -c /data/parameter/clades-def.txt -p $path -t 75  -o $path/results 
```

Here are some example outputs of this analysis:

![alt text][gt-portion]

[gt-portion]: example/figures/genetrees/Monophyletic_Bargraphs_Porportion.png ""


This figure shows the portion of RAxML genes for which important clades (x-axis) are highly (weakly) supported or rejected for three model conditions of plants dataset (Wickett, et al., 2014, PNAS). FAA-filterlen33: gene trees on amino acids sequences, and fragmentary sequences removed (66% gaps or more) FNA2AA-f25: amino acid sequences back translated to DNA, and sequences on long branches (25X median branch length)removed; FNA2AA-filterlen33: amino acid sequences back translated to DNA, and fragmentary sequences removed (66% gaps or more). Weakly rejected clades are those that are not in the tree but are compatible if low support branches (below 75%) are contracted.


![alt text][gt]

[gt]: example/figures/genetrees/Monophyletic_Bargraphs.png ""

This figure shows the number of RAxML genes for which important clades (x-axis) are highly (weakly) supported or rejected or are missing of three model conditions (same as above) of previously published dataset of plants (Wickett, et al., 2014, PNAS). Weakly rejected clades are those that are not in the tree but are compatible if low support branches (below 75%) are contracted. 


### 3. GC content analysis
* GC content analysis shows the ratio of GC content (to the number of A, C, G, T's) in first codon position, second codon position, third codon position, and all together across different species. For satisfying stationary assumption in DNA sequence evolution models, we expect that these ratios be close to identical across all species for each codon position separately. This might not be true for the third codon, which suggests removing the third codon position might help gene tree inferences.
* For GC content analysis use this structure **path/GENE_ID/DST-alignment-noFilter.fasta**, where **DST** defines the data sequence type (e.g FNA, NA, etc.), and DST-alignment-noFilter.fasta is the original sequence alignment without filtering. Please use the following command in bash:

```bash
./discoVista.py -p $path -m 2 -o $path/results 
```

* Using docker:

```bash
docker run -v <absolute path to data folder>:/data esayyari/discovista discoVista.py -p $path -m 2 -o $path/results 
```

Here are some example outputs of this analysis:


![alt text][gcpt]

[gcpt]: example/figures/GC/pTpP_GC_point.png ""


This figure corresponds to the GC content analysis of the 1kp dataset. Each dot shows the average GC content ratio for each species in all (red), first (pink), second (light blue), and third (dark blue) codon positions.

![alt text][gcpt]

[gcpt]: example/figures/GC/pTpP_GC_boxplot.png ""


This figure corresponds to the GC content analysis of the 1kp dataset, using boxplots for first, second, third, as well as all three codon positions.

### 4. Occupancy analysis
* To see the occupancy of different species or clades in different genes you would use this analysis. 
* For this analysis use this structure to have the sequence alignments, **path/GENE\_ID/DST-alignment-MODEL\_CONDITION.fasta**, where **MODE\_CONDITION** defines the model condition that the sequence is generated based on. Then you would use this command:

```bash
 ./discoVista.py -p $path -m 3 -a parameter/annotation.txt -o $path/results 
```
 
 * Using docker:

  
```bash
docker run -v <absolute path to data folder>:/data esayyari/discovista discoVista.py -p $path -m 3 -a /data/parameter/annotation.txt -o $path/results 
```
 
* If you want to have a tile graph that describes the occupancy of species for only one model condition you would use the option **-x DST-model\_condition**. For example, if you are interested in the occupancy map of your data and you used FNA as your DST in your directory names, and the model condition is noFiltered, then you can use this command: 
 
```bash
 ./discoVista.py -p $path -m 3 -a parameter/annotation.txt -x FNA-noFiltered -o $path/results 
```

* Using docker


```bash
docker run -v <absolute path to data folder>:/data esayyari/discovista discoVista.py -p $path -m 3 -a /data/parameter/annotation.txt -x FNA-noFiltered -o $path/results 
```
 
 
 
Here are some example outputs of this analysis:

![alt text][occ]

[occ]: example/figures/occupancy/occupancy.png ""

This figure shows the occupancy analysis on the 1kp dataset over each individual species for two model conditions (described above). 


 
![alt text][occ-clades]

[occ-clades]: example/figures/occupancy/occupancy_clades.png ""


This figure shows the occupancy analysis on the important splits of 1kp dataset over each individual species for two model conditions (described above). 

### 5. Branch support vs branch length analysis
* This analysis shows the correlation between the average of average gene MLBS values and average of average and maximum gene branch lengths for analyzing the long branch attraction and the effects of different inference methods on the reliability of gene trees. 
* First, organize gene trees using this structure **path/MODEL\_CONDITION/DST-estimated\_gene\_trees.tree**, where all estimated gene trees for the model condition are concatenated. Let's say that you have 3 model conditions, noFiltered, medFiltered, and highFiltered and you use FNA as your DST, then you would use the following code:

```bash
./discoVista.py -p $path -m 4  -r parameter/rootingDef.txt -o $path/results 
```

* Using docker:

* Using bash


```bash
docker run -v <absolute path to data folder>:/data esayyari/discovista discoVista.py -p $path -m 4  -r /data/parameter/rootingDef.txt -o $path/results 
```


### 6. Relative frequencey analysis
DiscoVista can show frequency of all three topologies around some focal branches of the infered species trees. These figures can be used to test amount of ILS, as well as if the conditions of ILS are met or not. Before describing the inputs and outputs of this analysis note that this analysis depends on DiscoVista branch of [ASTRAL](https://github.com/smirarab/ASTRAL/tree/DiscoVista), and in future version we will merge it with the master branch of ASTRAL. If you don’t want to deal with installation difficulties you would simply use DiscoVista docker image.

In order to run this analysis you need a folder (“-p”) under which you have your estimated species tree (with the name estimated_species_tree.tree) and your gene trees all in one file (with the name estimated_gene_trees.tree). For example, in the 1KP folder we have an estimated gene tree that has 844 genes in it. The rooting of them is not important. You need the output folder (“-o”), and you need an annotation file (“-a”) where you have one line per each species which assigns each species to a major split (clade) separated by tabs. There is an optional feature (“-g”) that you might specify the root of the tree you expect from your splits to it as well, e.g. Base or Outgroup.


The output will be similar figures to what we have under the results folder of examples. But it will generate 4 different figures. One of them is named tree.pdf which has 4 different ways of showing your summarized species tree based on your annotation file, and are your guide trees. Then we have the relativeFreq.pdf, which shows the frequency of three topologies around each focal internal branches of your summarized species tree. Here are example commands to run this analysis:

```bash
./discoVista.py -p $path -m 5 -a parameter/annotation-hypo.txt -o $path/results  -g Outgroup
```

using docker:

```bash
docker run -v <absolute path to data folder>:/data esayyari/discovista discoVista.py -p $path -m 5  -a /data/parameter/annotation-hypo.txt -o $path/results -g Outgroup
```


![alt text][relfreq]

[relfreq]: example/figures/relativeFreq/relativeFreq.png ""

This figure corresponds to the DiscoVista relative frequency analysis on 1kp dataset considering 4 different hypotheses. Frequency of three topologies around focal internal branches of ASTRAL species trees using the trimmed gene trees (removing alignments with more than 66% gap characters) on first and second codon positions of amino acid alignments back translated to DNA in 1kp dataset. Main topologies are shown in red, and the other two alternative topologies are shown in blue. The dotted lines indicate the 1/3 threshold. The title of each subfigure indicates the label of the corresponding branch on the tree on the right (also generated by DiscoVista). Each internal branch has four neighboring branches which could be used to represent quartet topologies. On the x-axis the exact definition of each quartet topology is shown using the neighboring branch labels separated by “\#”.



## Bug Reports
Please contact esayyari@ucsd.edu.
