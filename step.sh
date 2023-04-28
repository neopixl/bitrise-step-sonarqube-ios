#!/usr/bin/env bash

# retrieve value from bitrise 
xcode_project_path="${xcode_project_path}"
xcode_workspace_path="${xcode_workspace_path}"
app_scheme="${app_scheme}"
sonar_project_key="${sonar_project_key}"
sonar_host_url="${sonar_host_url}"
sonar_login="${sonar_login}"

# launch script
THIS_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python3 $THIS_SCRIPT_DIR/sonnar-ios-step.py $xcode_project_path $xcode_workspace_path $app_scheme $sonar_project_key $sonar_host_url $sonar_login
