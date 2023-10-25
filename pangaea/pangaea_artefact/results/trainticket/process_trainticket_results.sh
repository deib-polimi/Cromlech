#!/bin/bash

for i in *.csv
do
    echo ''
    echo ''
    echo '=== '$i' ==='
    cp $i ../../parser/annotations-parser/result.csv
    (cd ../../parser/annotations-parser/ && node run.js trainticket 1 10 27)
    (cd ../../parser/visualization/ && python3 create_microservices-data.py)
    cp ../../parser/visualization/microservices.json ../../output_converter/
    (cd ../../output_converter/ && python3 output_converter.py > 'trainticket_results/'${i%.*}.txt && rm microservices.json)
done
