#!/bin/bash
datawand init --name test_repo
echo
datawand list
echo
datawand create pipeline1
echo
datawand copy pipeline1.json pipeline2
echo
datawand status
echo
datawand delete pipeline1.json
echo
datawand delete pipeline2.json
echo
datawand scheduler start --port 8085
echo
python trial_parameters.py
echo
datawand view experiments/demo_1/Trial.json
echo
datawand view experiments/demo_1/Trial.json --name sample_CLONE_1
echo
datawand view experiments/demo_1/Trial.json --name sample_CLONE_2
echo
datawand view experiments/demo_1/Trial.json --name sample_CLONE_2
echo
datawand status
echo
datawand scheduler status
echo
datawand run experiments/demo_1/Trial.json --workers 1
datawand status
echo "Sleeping for 1 minutes"
sleep 60
datawand status
echo "Sleeping for 1 minutes"
sleep 60
datawand status
echo "Sleeping for 1 minutes"
sleep 60
datawand status
echo
datawand clear experiments/demo_1/Trial.json
echo
datawand scheduler stop
echo
datawand drop test_repo
echo "Done"
