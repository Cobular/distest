#!/usr/bin/env bash
source ./venv/bin/activate
python ./example_tester.py Cobular "$BOT_TOKEN" -c "$CHANNEL" -r all
