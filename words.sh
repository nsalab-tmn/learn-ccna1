#!/bin/bash

avg=120

for path in ./*/; do
    lmd_path=${path}lecture.md
    number_of_words=`wc --word < $lmd_path`
    number_of_minutes=$((number_of_words / avg))
    nom_lz=$(printf "%02d" $number_of_minutes)
    echo "$lmd_path": "$number_of_words" words - "$nom_lz" minutes of reading

    jmt_path=${path}learn-metadata.json
    cat "$jmt_path" | jq -r .duration
done
