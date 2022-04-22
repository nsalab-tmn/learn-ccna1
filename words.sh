#!/bin/bash

avg=120

for file in ./*/lecture.md; do
    number_of_words=`wc --word < $file`
    number_of_minutes=$((number_of_words / avg))
    echo "$file": "$number_of_words" words - "$number_of_minutes" minutes of reading
done
