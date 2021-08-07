#!/bin/sh

# -i matches upper and lower case; aha keeps the formatting
# TODO add functionality to replace spaces in $1 with -
grep -ri -C5 --color=always "$1" ../data/rfc | aha > ../data/match/$1.html
