#!/bin/bash

RD=2022/09/28

mkdir -p data_extracted/$RD
echo "" > data_extracted/$RD/ports.csv

function port_sum {
	ADDR=`echo $1 | grep -Po "(?<=\/)(\d+\.\d+\.\d+\.\d+)(?=.nmap.txt)"`
	PORT_SUM=`grep -Po "([0-9]+)(?=\/tcp\s*open.*)" $1`
	if [ -n "$PORT_SUM" ]; then 
		echo $ADDR $PORT_SUM >> data_extracted/$2/ports.csv
	fi
}

function port_open {
	grep -r "$1/tcp\s*open" data/$RD/*.nmap.txt \
		| cut -f 1 -d ':'
}

function extract_info {
	EINFO=$(grep -Pzo "$2\/tcp\s*open.*\n(?|\|.*\n)*\n*" $1 | tr -d '\0')
	ADDR=`echo $1 | grep -Po "(?<=\/)(\d+\.\d+\.\d+\.\d+)(?=.nmap.txt)"`
	if [ "$2" == "22" ]; then
		KEYS=(`echo "$EINFO" | grep -Pzo "(?<=ssh-hostkey:\s\n)(?:\|\s+\d+ .*\n)*(?:\|_\s+\d+ .*\n)" \
			| sed 's:[\|_\(\)]::g' | awk '{$1=$1};1' | sed 's:\s:-:g' \
			| tr -d '\0'`)
		if [ -n "$KEYS" ]; then
			source ./featuredb.sh
			init_db $2
			insert_features "${KEYS[@]}"
			echo $ADDR "${RET[@]}" >> data_extracted/$3/$2.csv
		fi
	fi
}

function process_file {
	if grep -q " open " "$1"; then
		echo "$1 contains useful info"
	fi
}

PORTS=(
	22
	80
	443
	8080	
)

echo "Extracting port info..."
find data/$RD -name '*.nmap.txt' -print0 \
	| xargs -0 -P 32 --max-procs=32 -I @ \
	bash -c "$(declare -f port_sum); port_sum @ $RD"

echo "Extract port feature..."
for PORT in "${PORTS[@]}"
do
	echo "Extracting feature of port $PORT..."
	echo "" > data_extracted/$RD/$PORT.csv
	port_open $PORT \
		| xargs -P 32 --max-procs=32 -I '{}' \
		bash -c "$(declare -f extract_info); extract_info {} $PORT $RD"
done


