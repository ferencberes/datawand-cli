#!/bin/bash
pushd examples/karate_club_demo

datawand init --name Demo
datawand list

datawand create GraphDemo
datawand add GraphDemo.json comet_key.txt
datawand add GraphDemo.json scripts/centrality.py
datawand add GraphDemo.json scripts/correlation.py
datawand view GraphDemo.json

datawand dependency add GraphDemo.json correlation centrality
datawand view GraphDemo.json --name correlation

python init_experiment.py
datawand status

datawand view experiments/demo/GraphDemo.json
datawand view experiments/demo/GraphDemo.json --name correlation_CLONE_2

datawand scheduler start
datawand scheduler status

datawand run experiments/demo/GraphDemo.json --workers 2

echo "Sleeping for 30 seconds"
sleep 30

datawand status
datawand log experiments/demo/GraphDemo.json --name correlation_CLONE_2 --tail 5

datawand scheduler stop
datawand delete GraphDemo.json
datawand drop Demo

rm -r experiments
popd