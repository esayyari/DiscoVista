# DiscoVista

DiscoVista (Discordance Visualization Tool) is a python and R-based software utility to analyze and visualize the phylogenetic information and gene discordances. 

#INSTALLATION:
The software package __DiscoVista__ depends on some R and python packages. You could install __DiscoVista__ in a couple of steps:

Clone to [__DiscoVista__](https://github.com/esayyari/DiscoVista) git repository or download [this](https://github.com/esayyari/DiscoVista/archive/master.zip) zip file.
Then you need to set environmental variable __WS_HOME__ to the directory under which this __DiscoVista__ repository is placed. 

##R dependencies
There are some R packages that you need to install at this step. The R package dependencies are: __Reshape__, __Reshape2__, __ggplot2__, __plyr__, __scales__, and __optparse__.

To install these packages you need to use the following command:

~~~R
install.packages(c("Reshape","Reshape2","ggplot2","plyr","scales","optparse"))
~~~

##Python dependency
You need to install __DendroPy__ as well. In Mac or Linux, you would use __pip__ to install DendroPy. If you have root access, you could use:

~~~bash
sudo pip install dendropy
~~~

otherwise, you would install dendropy with the command:

~~~bash
pip install dendropy --user
~~~

##How DiscoVista works

The main file to run the analysis is __discoVista.py__. To use this utility in bash you would use: 

~~~
Usage: discoVista.py [options]

Options:
  -h, --help                                Show this help message and exit
  -a ANNOTATION, --annotation=ANNOTATION     The annotation file
  -c CLADES, --clades=CLADES                The path to the clades definition file
  -m MODE, --mode=MODE                      Determines which analysis to be done.
                                              To do discordance analysis on species tree use 0. To do discordance analysis on 
                                              gene trees use 1. For GC stat analysis use -m 2. 
                                              For occupancy analysis use -m 3. doing MLBS vs 
                                              branch length analysis use -m 4.
  -p PATH, --path=PATH                      Path to the gene directory or species tree
  -r ROOT, --rooting=ROOT                    The rooting file
  -s STYLE, --style=STYLE                    The color style file
  -t THRESH, --threshold=THRESH                The bootstrap threshold
  -x MODELCOND, --modelCond=MODELCOND        The model condition that the occupancy map 
                                              will be plotted for
~~~ 

There are some files that you need to run analyses. <a name="somefiles"></a>

1. You would pass the annotation file to the utility using **-a ANNOTATION**. In each line of this file, you need the taxon name and the corresponding clade name that species belongs to. Please use tab as the separator. 
2. You would pass the rooting definition file to the utility using **-r ROOT**. Let's say that you have an **outgroup** clade. On the lines of this file, the set of species in the order of speciation events time are listed. The set of species on the first line belongs to the species that are the most distant species to the ingroup species. The next line belongs species in the outgroup which are the second most distant species to the ingroup species, and so on. 
3. You would pass the clade definition file to the utility using **-c CLADE**. There is an example of this file available under the DiscoVista GitHub repository. Also, there is another tool to generate this clade definition file in this repository under DiscoVista/src/utils/generate_clade-defs.py. 

### How to generate clade definition file
Clade definition file has different columns. The column names are: __Clade Name__, __Clade Definition__, __Section Letter__ , __Components__,    __Show__, and    __Comments__.

* __Clade Name__ defines the name of clade
* __Clade Definition__ is the list of species or other clades in this clade. You would use **+** or **-** signs to define them.
* __Section Letter__ Name that will define the order of clades. If there is no ordering between clades leave it blank. 
* __Components__ The list of important species or clades that defines the clade. If one of these species or clades is missed, the clade will be considered as missing.
* __Show__ This is a 0/1 variable. If this is 1 that clade will be considered for the analyses, otherwise this clade will not be considered. 
* __Comments__ comments about the clade.

Also, there is the python code **generate_clade-defs.py** that could be used to generate the clade definition file from the annotation file. You would use it using the command:

~~~bash
generate_clade-defs.py [annotation file] [outputfile] [important branches file]
~~~

In important branches file, you could define other important branches of the expected tree. Let's say that we have two clades **A**, and **B**, and you are interested in the branch that separates **AB** from others. Then you would define it with **A+B** in this file.

## How to run DiscoVista
Throughout this tutorial, we assume that you are using bash, and your current directory is **WS\_HOME/DiscoVista/**. The rooting definitions are listed in rooting.txt, the annotation file is annotation.txt, and the clade definition file is clade-definition.txt (as described [above](#somefiles)).  

### 1. Discordance analysis on species trees
To perform discordance analysis on gene trees, you need rooted gene trees with the MLBS values  [local posterior probabilities] (https://github.com/smirarab/ASTRAL) draw on the branches and represented in Newick format as node labels. For drawing MLBS on branches we highly recommend using [newick utilities](http://cegg.unige.ch/newick_utils). 

* Species trees should be stored following this structure **path/MODEL\_CONDITION-DST/estimated\_species\_tree.tree**. Here __path__ points to the directory that species trees are located. Put each estimated species tree inferred with different methods under different directories. The name of these directories should follow **model\_condition-data\_sequence\_type**. For example, if you have different filtering strategies for your nucleotide acid sequences and then the gene trees are inferred using [RAxML](http://sco.h-its.org/exelixis/web/software/raxml/index.html), you might put the species tree with name estimated\_species\_tree.tree, under RAxML\_highly\_filtered-NA.  Please only use **"-"** to separate the model condition from the data sequence type.

* Let's assume that the MLBS values are drawn on branches of the species tree available at path \$path, and there are 3 model conditions, RAxML\_highly\_filtered-NA, RAxML\_med\_filtered-NA, and RAxML\_highly\_filtered-NA. Also, assume that you consider branches with MLBS above 75 as highly supported branches, and the code will contract branches below that. Then you would call the software in bash using the following command:

~~~bash
./discoVista.py -m 0 -a annotation.txt -c clades-def.txt -p $path -r rootingDef.txt -t 75  
~~~

* If you are using local posterior probabilities instead of MLBS, and let's assume that the branches above the threshold of 0.95 considered as highly supported branches, then you would use the software with:

~~~bash
./discoVista.py -m 0 -a annotation.txt -c clades-def.txt -p $path -r rootingDef.txt -t 0.95
~~~


### 2. Discordance analysis on gene trees

To perform discordance analysis on gene trees, you need rooted gene trees with the MLBS values draw on the branches and represented in Newick format as node labels. For drawing MLBS on branches we highly recommend using [newick utilities](http://cegg.unige.ch/newick_utils). 

* Gene trees should be stored using this structure **path/GENE\_ID/GENE\_ID-MODEL\_CONDITION-DST/estimated\_gene\_trees.tree**. Here __path__ points to the directory that gene trees are located. Please only use **"-"** to separate the gene ID, model condition, and data sequence type. Put each estimated gene tree inferred with different methods for the different gene under different directories. The name of these directories should follow **GENE\_ID-model\_condition-data\_sequence\_type**. 

* Note that you would do this analysis for each model condition separately. 

* Let's assume that the MLBS values are drawn on branches of the gene trees of model condition RAxML\_highly\_filtered-NA available at path \$path. Also, assume that you consider branches with MLBS above 75 as highly supported branches, and the code will contract branches below that. Then you would call the software in bash using the following command:

~~~bash
./discoVista.py -m 1 -a annotation.txt -c clades-def.txt -p $path -r rootingDef.txt -t 75  
~~~



### 3. GC content analysis
* GC content analysis shows the ratio of GC content (to the number of A, C, G, T's) in first codon position, second codon position, third codon position, and all together across different species. For satisfying stationary assumption in DNA sequence evolution models, we expect that these ratios be close to identical across all species. 
* For GC content analysis use this structure **path/GENE_ID/DST-alignment-noFilter.fasta**, where **DST** defines the data sequence type (e.g FNA, NA, etc.), and DST-alignment-noFilter.fasta is the original sequence alignment without filtering. Please use the following command in bash:

~~~bash
./discoVista.py -p $path -m 2 -a annotation.txt
~~~

### 4. Occupancy analysis
* To see the occupancy of different species or clades in different genes you would use the following commands. 
* First for this analysis use this structure to have the sequence alignments, **path/GENE\_ID/DST-alignment-MODEL\_CONDITION.fasta**, where **MODE\_CONDITION** defines the model condition that the sequence is generated based on. Then you would use this command:
 
 ~~~bash
 ./discoVista.py -p $path -m 3 -a annotation.txt 
 ~~~
 
 If you want to have a tile graph that describes the occupancy of species for only one model condition you would use the option **-x DST-model\_condition**. For example, if you are interested in the occupancy map of your data and you used FNA as your DST in your directory names, and the model condition is noFiltered, then you can use this command: 
 
 ~~~bash
 ./discoVista.py -p $path -m 3 -a annotation.txt -x FNA-noFiltered
 ~~~
### 5. Branch support vs branch length analysis
* This analysis shows the correlation between the average of average and maximum gene MLBS values versus the average of average gene branch lengths for tracking the long branch attraction and the effects of different inference methods on MLBS. 
* First organize gene trees using this structure **path/MODEL\_CONDITION/DST-estimated\_gene\_trees.tree**, where all estimated gene trees for the model condition are concatenated. Let's say that you have 3 model conditions, noFiltered, medFiltered, and highFiltered and you use FNA as your DST, then you would use the following code:

~~~bash
./discoVista -p $path -m 4 -a annotation.txt -r root.txt
~~~

