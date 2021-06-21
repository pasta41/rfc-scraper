#!/bin/sh
grep -lri $1 ../data/rfc/ > ../data/match/$1.txt
