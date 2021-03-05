#!/usr/bin/env bash
  if [[ $(cd docs && make testhtml | grep warning) ]]; then
      echo "There were errors"
      exit 1
  else
      echo "Docs compiled without any warnings or errors!"
      exit 0
  fi
