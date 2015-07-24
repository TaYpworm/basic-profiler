#!/bin/bash

# Used as a basic mechanism to profile a program's cpu and memory usage.
# Script outputs process information at regular intervals to a file and screen.
# File output will be appended to "profile.out" or command line specified file.
# Should shut down when process being watched stops.

INTERVAL=1
OUTFILE=profile.out
PID=

# Process command line options.
# -i = watch interval in seconds
# -o = output file name
# -p = pid to watch
while getopts i:o:p: opt; do
	case $opt in
	i)
		INTERVAL=$OPTARG
		;;	
	o)
		OUTFILE=$OPTARG
		;;
	p)
		PID=$OPTARG
		;;
	esac
done

# Fail if PID not set
if [ -z "$PID" ]; then
	echo "PID not set"
	exit 1
fi

# Grab the second line of PS output and send it to the output file and screen.
watch -e -n $INTERVAL "ps o pid,pcpu,cputime,etime,size,rss,vsz,cmd -p $PID | awk 'NR==2' | tee -a $OUTFILE"
