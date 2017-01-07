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
                                              gene trees use 1. For GC stat analysis use 2. 
                                              For occupancy analysis use 3. doing MLBS vs 
                                              branch length analysis use 4.
  -p PATH, --path=PATH                      Path to the gene directory or species tree
  -r ROOT, --rooting=ROOT                    The rooting file
  -s STYLE, --style=STYLE                    The color style file
  -t THRESH, --threshold=THRESH                The bootstrap threshold
  -x MODELCOND, --modelCond=MODELCOND        The model condition that the occupancy map 
                                              will be plotted for
~~~ 

There are some files that you need to run analyses. 

1. You would pass the annotation file to the utility using **-a ANNOTATION**. In each line of this file, you need the taxon name and the corresponding clade name that species belongs to. Please use tab as the seperator. 
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

## The structure of data for different analyses

* For discordance analysis on species trees you need this structure
    **path/MODEL\_CONDITION-DST/estimated\_species\_tree.tree**. Where __path__ is the path that all the species trees inferred with different methods are. Put each estimated species tree inferred with different methods under different directories. The name of this directory is in this structure **model\_condition-data\_sequence\_type**. Please only use **"-"** to separate the model condition from the data sequence type. 
* For discordance analysis on gene trees you need this structure **path/GENE\_ID/GENE\_ID-MODEL\_CONDITION-DST/estimated\_gene\_trees.tree**. Please only use **"-"** to separate the gene ID, model condition, and data sequence type. 
* For GC content analysis use this structure **path/GENE_ID/DST-alignment-noFilter.fasta**, where **DST** defines the data sequence type.
* For occupancy analysis use this structure **path/GENE\_ID/DST-alignment-MODEL\_CONDITION.fasta**, where **MODE\_CONDITION** defines the model condition that the sequence is generated based on. 
* For branch support vs branch length analysis put gene trees using this structure **path/MODEL\_CONDITION/DST-estimated\_gene\_trees.tree**. In estimated gene trees files concatenate all the estimated trees. 
