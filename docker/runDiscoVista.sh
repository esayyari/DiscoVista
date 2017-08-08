#!/bin/bash


show_help() { 
cat << EOF
	This is DiscoVista!
	These are enviromentent variables that you would set inside the env.list:
		HELP		show help
		ANOT		annotation file
		CLAD		clade defenition 
		MODL		The analysis that you would do
		ROOT		Th rooting defenition
		NEWO		The new ordering of clades defenition file
		NEWM		The new ordering of the different model conditions file
		THRS		The threhsold that defines the high support branchs
		MISS		Defines if having missing clade or species is allowed in the 
				species tree analysis
		COND		The modle condition which the occupancy map will be created
		DS		The label that you use for the relative frequency analysis
		NAME		The nameing file
	If you want to run everything in the interactive mode use the following command:
	    docker run -it discoVista --env-file <env.list> -v <data on your machine>:/data
    	If you want to test the DiscoVista, please download the sample data from the DiscoVista 
	git reposiotry https://github.com/esayyari/DiscoVista/blob/master/example/1KP.zip.
	   Unzip this archive on your machine. Then use the proper set of enviromentent variables
	for each of the analyses:
	Assume that you are under the 1KP folder after unzipping. 
	To see the help use:
	    docker run --env HELP=1 discoVista
	Use these commands for the analysis:
	The species tree discordance analysis	
	    docker run --env-file env0.list -v <path to 1KP example folder>/1KP:/data discoVista 
	The gene trees discordance analysis
	    docker run --env-file env1.list -v <path to 1KP example folder>/1KP:/data discoVista
	The GC content analysis
	    docker run --env-file env2.list -v <path to 1KP example folder>/1KP:/data discoVista
	The occupancy analysis
	    docker run --env-file env3.list -v <path to 1KP example folder>/1KP:/data discoVista
	The branch support vs branch length analysis 
   	    docker run --env-file env4.list -v <path to 1KP example folder>/1KP:/data discoVista
	The relative frequency analysis
	    docker run --env-file env5.list -v <path to 1KP example folder>/1KP:/data discoVista
	For your usage you can replace <path to 1KP example folder> with the path to your data
	   directory, and update the env.list that suits your analysis. 
	
EOF
}

if [ "$HELP" != "" ] && [ "$HELP" -eq "1" ]; then
	show_help
	exit 0
fi




if [ "$DIR" != "" ]; then
	cd $DIR
fi

if [ "$PTH" != "" ]; then
	echo "$PTH"
fi

disco=$WS_HOME/DiscoVista/src/utils/discoVista.py

if [ "$MISS" == "" ] || [ "$MISS" -eq "0" ]; then
	ms=0
else
	ms=1
fi	

if [ "$MODL" != "" ]; then
	if [ "$MODL" -eq "0" ] || [ "$MODL" -eq "1" ]; then
		if [ "$NEWO" != "" ] && [ "$NEWM" != "" ]; then
			cmd="$disco -m $MODL -p $PTH -t $THRS -r $ROOT -c $CLAD -a $ANOT -y $NEWMD -w $NEWOR -k $ms"
		elif [ "$NEWO" != "" ] && [ "$NEWM" == "" ]; then
			cmd="$disco -m $MODL -p $PTH -t $THRS -r $ROOT -c $CLAD -a $ANOT -w $NEWOR -k $ms"
		elif [ "$NEWO" == "" ] && [ "$NEWM" != "" ]; then 
			cmd="$disco -m $MODL -p $PTH -t $THRS -r $ROOT -c $CLAD -a $ANOT -y $NEWMD -k $ms"
		else
			cmd="$disco -m $MODL -p $PTH -t $THRS -r $ROOT -c $CLAD -a $ANOT -k $ms"
		fi
	elif [ "$MODL" -eq "2" ]; then
		cmd="$disco -m $MODL -p $PTH -a $ANOT"
	elif [ "$MODL" -eq "3" ]; then
		cmd="$disco -m $MODL -p $PTH -a $ANOT"
	elif [ "$MODL" -eq "4" ]; then
		if [ "$COND" == "" ]; then
			cmd="$disco -m $MODL -p $PTH -r $ROOT -a $ANOT -x $COND"
		else
			cmd="$disco -m $MODL -p $PTH -r $ROOT -a $ANOT"
		fi
	elif [ "$MODL" -eq "5" ]; then

		cmd="$WS_HOM/DiscoVista/src/tools/pos-for-hyp.sh $PTH $ANOT $NAME  $DS"
	fi
else
	show_help
	exit 0
fi

echo $cmd
#bash -c "$cmd"

