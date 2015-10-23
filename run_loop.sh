#!/bin/bash


Protocol=$1
NClusters=$2
Weight=$3

echo "Protocol: "$Protocol"\n"
echo "NClusters: "$NClusters"\n"
echo "Weight: "$Weight"\n"


Dir="../related_files/"${Protocol}"/ClusterResult_"${NClusters}

ProgramDir=`pwd`

Kth=0
while [[ $Kth -lt $NClusters ]]
do
	echo "Aligning the cluster "$Kth" ...\n"
	#cd Dir
	#touch "signature_"$Kth".txt"
	#cd ProgramDir
	nohup ./main.py -w $Weight -h $Dir"/cluster_"$Kth".txt" &
	Kth=`expr $Kth + 1`
	echo $Kth
	
done

echo "All the clusters aligned.\n"






