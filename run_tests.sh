#!/usr/bin/env bash

python example_target.py "$TARGET_TOKEN" &

sleep 5s

python example_tester.py "$TARGET_NAME" "$TESTER_TOKEN" -c "$CHANNEL" -r all