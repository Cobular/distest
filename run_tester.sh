#!/usr/bin/env bash
source ./venv/bin/activate
# Includes my user ID here for testing
python ./example_tester.py "249705405372956672" "$BOT_TOKEN" -c "$CHANNEL" -r all
