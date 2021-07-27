#!/bin/bash

# first arg should be the file to read from
# second arg should be the file path (no trailing /) to
# find the files in
# third arg should be the directory to cp the files to
# (no trailing /)

while read -r line; do
	# convert to pdf
	enscript -p "output.ps" "$2/rfc$line.txt"
	ps2pdf "output.ps" "$2/rfc$line.pdf"
    mv "$2/rfc$line.pdf" "$3/"
done < "$1"
rm "output.ps"
