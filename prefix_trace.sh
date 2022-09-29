#!/bin/bash

CURDATE=`date '+%Y/%m/%d'`

MAX_THREADS=24

PREFIX_LIST=(
	202.112.14.0/23
	218.194.32.0/19
	202.115.0.0/19
	211.83.96.0/20
	210.41.96.0/20
	222.197.160.0/19
	121.48.152.0/21
	121.48.160.0/20
	121.49.64.0/18
	113.54.128.0/17
)

function do_list {
	nmap -sL -n $1 | awk '/Nmap scan report/{print $NF}' | xargs -P $MAX_THREADS --max-procs=$MAX_THREADS -i ./trace.sh '{}' $CURDATE
}

mkdir -p data/$CURDATE

for pfx in "${PREFIX_LIST[@]}"
do
	echo "Scanning prefix $pfx"
	do_list $pfx
done

echo "All scans done."
