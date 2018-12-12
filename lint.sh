#!/usr/bin/env bash

# Sensors
for sensor in ./sensor/*.py; do
  isort "$sensor"
  flake8 "$sensor"
  autopep8 --in-place --aggressive "$sensor"
done
