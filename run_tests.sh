#!/usr/bin/env bash

python example_target.py "$TARGET_TOKEN" &

sleep 5s

python example_tester.py "$TARGET_ID" "$TESTER_TOKEN" -c "$CHANNEL" -r all

python example_target_ext_commands.py "$TARGET_TOKEN" TESTING &

sleep 5s

python example_tester_ext_commands.py "$TARGET_ID" "$TESTER_TOKEN" -c "$CHANNEL" -r all
