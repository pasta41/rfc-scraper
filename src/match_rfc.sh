#!/bin/sh
grep -rli $1 ../data/rfc > ../data/match/$1.txt
