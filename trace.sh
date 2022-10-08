#!/bin/bash

function do_ping {
	ping -i 0.4 -c 3 -w 2 $1 > /dev/null 2>&1
}

function do_trace {
	mtr $1 -c 3 -n -C -G 1 -T
}

function do_scan {
	nmap -T 5 -F \
		-sV -version-all -O -sC \
		-n -Pn \
		$1 \
		-oN $2 \
		> /dev/null 2>&1
}

CURDATE=$2

if do_ping $1; then
	echo "Scanning IP $1"
	do_trace $1 > data/$CURDATE/$1.path.txt
	do_scan $1 data/$CURDATE/$1.nmap.txt
else
	echo "IP $1 is down."
fi