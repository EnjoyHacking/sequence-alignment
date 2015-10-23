#!/bin/bash

#./main.py -w $1 -g -a http.raw 
#./main.py -p ~/PcapData/Pure/pure_http.pcap 
#./main.py -h ../related_files/http/ClusterResult_10/cluster_0.txt 
#./main.py -h ../related_files/http/ClusterResult_10/cluster_1.txt 
#nohup ./main.py -w 0.8 -h ../related_files/http/ClusterResult_10/cluster_1.txt  &



nohup ./main_mp.py -w 0.8 -h ../related_files/http/ClusterResult_10/ &
