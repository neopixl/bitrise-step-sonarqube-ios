#!/usr/bin/env bash

# retrieve script directory
THIS_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# launch script
python3 $THIS_SCRIPT_DIR/sonnar-ios-step.py 
