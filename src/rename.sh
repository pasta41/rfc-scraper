for f in *.txt; do
    mv -- "$f" "rfc${f}"
done
