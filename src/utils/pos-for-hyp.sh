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

outgroup=$5

d=$(dirname $species)

mkdir -p $d/$out || true
out=$d/$out
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

f=$(cat $WS_HOME/ASTRAL/.git/HEAD | grep -o "DiscoVista")
if [ "$f" != "DiscoVista" ]; then
	echo "please use branch DiscoVista with the command git checkout DiscoVista"
	exit 1
fi
pushd .
cd $WS_HOME/ASTRAL
V=$(git ls-tree -r DiscoVista | grep "Astral.*zip" | awk '{print $NF}'| sed -e 's/Astral/astral/' | sed -e 's/.zip/.jar/')
popd

astral=$(find $WS_HOME/ASTRAL/$V)
java -jar $astral -i $genes -q $d/$name-hypo.tre -t 16 -o  $d/$name-uncollapsed.tre

sed -i "s/)N\([0-9][0-9]*\)'/)'N\1/g" $d/$name-uncollapsed.tre

python $WS_HOME/DiscoVista/src/utils/spit-hypo-trees.py $d/$name-uncollapsed.tre $ant collapse

cp $d/$name-uncollapsed.tre-collapsed.tre $d/$name.tre

sed -i  "s/)'N\([0-9][0-9]*\)[^']*'/)N\1/g" $d/$name.tre

nw_reroot $d/$name.tre "$outgroup" > $d/$name.tre.rerooted

mv $d/$name.tre.rerooted $d/$name.tre

printf "$WS_HOME/DiscoVista/src/utils/display.py $d/$name.tre\n"

$WS_HOME/DiscoVista/src/utils/display.py $d/$name.tre $outgroup

#nw_display -S -s $d/$name.tre.out > $d/$name.svg

printf  "python $WS_HOME/DiscoVista/src/utils/map_names.py $names $annot $d/freqQuad.csv $d/freqQuadCorrected.csv $d/$name.tre.out\n"

python $WS_HOME/DiscoVista/src/utils/map_names.py $names $annot $d/freqQuad.csv $d/freqQuadCorrected.csv $d/$name.tre.out

cd $d

Rscript --vanilla freqQuadVisualization.R
$WS_HOME/DiscoVista/src/R/plotTree.R $d/$name.tre.out
