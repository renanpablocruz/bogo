#!/bin/bash

count=53985

for file in *.extension
do
    new=$(printf "%05d.sgf" "$count")
    mv -- "$file" "$new"
    (( count++ ))
done
