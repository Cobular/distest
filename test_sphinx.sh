#!/usr/bin/env bash
if [[ $(git diff HEAD^ HEAD | grep docs/source) ]]; then
    echo "Docs Changed"
    if [[ $(cd docs && make testhtml | grep warning) ]]; then
        echo "There were errors"
        exit 1
    else
        echo "Docs compiled without any warnings or errors!"
        exit 0
    fi
else
    echo "Docs Didn't Change, Nothing to Test"
    exit 0
fi