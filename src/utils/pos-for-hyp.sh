#!/bin/bash

echo "USAGE: [PATH] [annotation] [names] [OUTDIR] [label] [outgroup]"

name=main
pth=$1

species=$pth/estimated_species_tree.tree
genes=$pth/estimated_gene_trees.tree
annot=$2
names=$3
out=$4
name="main"
if [ "$#" -eq "5" ]; then
	
	outgroup=""
else
	outgroup=$5
fi

d=$(dirname $species)

mkdir -p $out || true
cp $species $out/
cp $genes $out/
cp $annot $out/
cp $names $out/

cd $out/

species=$(basename $species)
genes=$(basename $genes)
annot=$(basename $annot)
names=$(basename $names)


echo "Code	Hypo" > $annot.with.header.txt
cat $annot >> $annot.with.header.txt

ant=$(find $annot.with.header.txt)


python $WS_HOME/DiscoVista/src/utils/spit-hypo-trees.py $species  $ant contract

d=`pwd`;

cp $species-hypo.tre $d/$name-hypo.tre


astral=$WS_HOME/DiscoVista/bin/astral.4.10.12.jar
java -jar $astral -i $genes -q $d/$name-hypo.tre -t 16 -o  $d/$name-uncollapsed.tre

sed -i "s/)N\([0-9][0-9]*\)'/)'N\1/g" $d/$name-uncollapsed.tre

python $WS_HOME/DiscoVista/src/utils/spit-hypo-trees.py $d/$name-uncollapsed.tre $ant collapse

cp $d/$name-uncollapsed.tre-collapsed.tre $d/$name.tre

sed -i  "s/)'N\([0-9][0-9]*\)[^']*'/)N\1/g" $d/$name.tre

if [ "$outgroup" != "" ]; then
	nw_reroot $d/$name.tre "$outgroup" > $d/$name.tre.rerooted
	mv $d/$name.tre.rerooted $d/$name.tre
fi



printf "$WS_HOME/DiscoVista/src/utils/display.py $d/$name.tre\n"

if [ "$outgroup" != "" ]; then
	$WS_HOME/DiscoVista/src/utils/display.py $d/$name.tre $outgroup
else
	$WS_HOME/DiscoVista/src/utils/display.py $d/$name.tre
fi


printf  "python $WS_HOME/DiscoVista/src/utils/map_names.py $names $annot $d/freqQuad.csv $d/freqQuadCorrected.csv $d/$name.tre.out\n"

python $WS_HOME/DiscoVista/src/utils/map_names.py $names $annot $d/freqQuad.csv $d/freqQuadCorrected.csv $d/$name.tre.out

cd $d

Rscript --vanilla freqQuadVisualization.R
$WS_HOME/DiscoVista/src/R/plotTree.R $d/$name.tre.out
