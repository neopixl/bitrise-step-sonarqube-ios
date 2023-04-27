#!/usr/bin/env bash

# retrieve value from bitrise 
xcode_project_path="${xcode_project_path}"
xcode_workspace_path="${xcode_workspace_path}"
app_scheme="${app_scheme}"
sonar_project_key="${sonar_project_key}"
sonar_host_url="${sonar_host_url}"
sonar_login="${sonar_login}"

# launch script
/usr/bin/python3 -c "$(wget -q -O - https://raw.githubusercontent.com/neopixl/bitrise-step-sonarqube-ios/feature/new-sonnar-scanner/sonnar-ios-step.py $xcode_project_path $xcode_workspace_path $app_scheme $sonar_project_key $sonar_host_url $sonar_login)"




