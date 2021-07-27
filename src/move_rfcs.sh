#!/bin/bash

# first arg should be the file to read from
# second arg should be the file path (no trailing /) to
# find the files in
# third arg should be the directory to cp the files to
# (no trailing /)

while read -r line; do
	FILENAME="$2/rfc$line.txt"
    cp "$FILENAME" "$3/"
done < "$1"
