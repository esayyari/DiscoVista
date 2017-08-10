#!/bin/bash

echo "USAGE: [ASTRAL species tree] [gene trees] [tree 2]"


astral=$1
genetree=$2
tree2=$3
d=$(dirname $astral)

f=$(cat $WS_HOME/ASTRAL/.git/HEAD | grep -o "master")
if [ "$f" != "master" ]; then
	echo "please use branch master with the command git checkout master"
	exit 1
fi
pushd .
cd $WS_HOME/ASTRAL
V=$(git ls-tree -r master | grep "Astral.*zip" | awk '{print $NF}'| sed -e 's/Astral/astral/' | sed -e 's/.zip/.jar/')
popd

astralcommand=$(find $WS_HOME/ASTRAL/$V)

java -jar $astralcommand -i $genetree -q $astral -t 3 -o $astral.scored 

$WS_HOME/global/src/shell/compareTrees $astral.scored $tree2 | grep -v "-" | awk '{print $1,$2,$3,$4,$6,$7}'> $d/compare.csv



