#!/bin/bash

RD=2022/09/28

mkdir -p data_extracted/$RD
touch data_extracted/$RD/paths.csv

TOT=`ls data/$RD/*.path.txt | wc -l`
CNT=0

function process_file {
        {
        PREV=
        read
        while IFS= read -r line
        do
                CURIP=`echo "$line" | cut -f 6 -d ','`
                if [ ! -z "$PREV" ]; then
                        echo "$PREV,$CURIP" >> data_extracted/$2/paths.csv
                fi
                PREV=$CURIP
        done
        } < "$1"
}

find data/$RD -name '*.path.txt' -print0 \
	| xargs -0 -P 32 --max-procs=32 -I @ \
	bash -c "$(declare -f process_file); process_file @ $RD"

cat data_extracted/$RD/paths.csv | sort | uniq > data_extracted/$RD/paths.processed.csv
