#!/usr/bin/env bash

set -ex

rm -rf src/yogaflo.egg-info build dist
python3 setup.py sdist bdist_wheel

twine upload dist/*
