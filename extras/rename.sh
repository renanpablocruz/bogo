#!/bin/bash

count=1

for file in *.sgf
do
    new=$(printf "%05d.sgf" "$count")
    mv -- "$file" "$new"
    (( count++ ))
done
