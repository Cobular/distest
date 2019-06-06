#!/usr/bin/env bash

python example_target.py $TARGET_TOKEN &

sleep 5s

python example_tester.py $TARGET_NAME $TESTER_TOKEN -c 586041924129914910 -r all