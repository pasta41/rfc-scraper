#!/bin/sh
# TODO add functionality to replace spaces in $1 with -
grep -rli "$1" ../data/rfc > ../data/match/$1.txt
