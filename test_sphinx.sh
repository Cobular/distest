#!/usr/bin/env bash
if [[ $(git diff | grep docs/source) ]]; then
    echo "Docs Changed"
else
    echo "Docs Didn't Change"
fi