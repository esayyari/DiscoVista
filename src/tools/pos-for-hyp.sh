#!/bin/bash

echo "USAGE: [species tree] [gene tree] [annotation] [names] [data set] [OUTGROUP]"


name=main
species=$1
genes=$2
annot=$3
#rooting=$4
names=$4
DS=$5
outgroup=$6

echo "Code	Hypo" > $annot.with.header.txt
cat $annot >> $annot.with.header.txt
ant=$(find $annot.with.header.txt)
#$WS_HOME/DiscoVista/src/utils/root-nw_friendly.py $species $rooting 

#species=$species.rerooted

python $WS_HOME/DiscoVista/src/tools/spit-hypo-trees.py $species  $ant contract

d=$(dirname $species);

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
#sed -i 's/_/ /g' $d/freqQuad.csv
#set -x

sed -i "s/)N\([0-9][0-9]*\)'/)'N\1/g" $d/$name-uncollapsed.tre
python $WS_HOME/DiscoVista/src/tools/spit-hypo-trees.py $d/$name-uncollapsed.tre $ant collapse
cp $d/$name-uncollapsed.tre-collapsed.tre $d/$name.tre
sed -i  "s/)'N\([0-9][0-9]*\)[^']*'/)N\1/g" $d/$name.tre
echo $outgroup
nw_reroot $d/$name.tre "$outgroup" > $d/$name.tre.rerooted
$WS_HOME/DiscoVista/src/tools/display.py $d/$name.tre.rerooted
nw_display -S -s $d/$name.tre.rerooted.out > $d/$name.svg
echo python $WS_HOME/DiscoVista/src/utils/map_names.py $names $annot $d/freqQuad.csv $d/freqQuadCorrected.csv $DS $d/$name.tre.rerooted.out
python $WS_HOME/DiscoVista/src/utils/map_names.py $names $annot $d/freqQuad.csv $d/freqQuadCorrected.csv $DS $d/$name.tre.rerooted.out
cd $d
Rscript --vanilla freqQuadVisualization.R
$WS_HOME/DiscoVista/src/R/plotTree.R $d/$name.tre.rerooted.out
