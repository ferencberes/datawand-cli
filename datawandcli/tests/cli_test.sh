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
datawand scheduler start --port 8085 --keep 1800 --retry 900
echo
python trial_parameters.py
echo
datawand view experiments/demo_1/Trial.json
echo
datawand view experiments/demo_1/Trial.json --name PySample_CLONE_1
echo
datawand view experiments/demo_1/Trial.json --name PySample_CLONE_2
echo
datawand view experiments/demo_1/Trial.json --name PySample_CLONE_2
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
datawand log experiments/demo_1/Trial.json --tail 10
datawand log experiments/demo_1/Trial.json --name PySample_CLONE_1
datawand log experiments/demo_1/Trial.json --name PySample_CLONE_2 --tail 30
datawand log experiments/demo_1/Trial.json --name PySample_CLONE_3 --all
echo
datawand clear experiments/demo_1/Trial.json
echo
datawand scheduler stop
echo
datawand drop test_repo
echo "Done"
