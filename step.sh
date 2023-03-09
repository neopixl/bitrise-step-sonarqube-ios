#!/bin/bash
set -e

# Global parameters
SWIFTLINT_CMD=swiftlint
XCPRETTY_CMD=xcpretty
XCODEBUILD_CMD=xcodebuild

trap "echo 'Script interrupted by Ctrl+C'; stopProgress; exit 1" SIGHUP SIGINT SIGTERM

function startProgress() {
	while true
	do
    	echo -n "."
	    sleep 5
	done
}

function stopProgress() {
	if [ "$vflag" = "" -a "$nflag" = "" ]; then
		kill $PROGRESS_PID &>/dev/null
	fi
}

function testIsInstalled() {

	hash $1 2>/dev/null
	if [ $? -eq 1 ]; then
		echo >&2 "ERROR - $1 is not installed or not in your PATH"; exit 1;
	fi
}

# Run a set of commands with logging and error handling
function runCommand() {

	# 1st arg: redirect stdout
	# 2nd arg: command to run
	# 3rd..nth arg: args
	redirect=$1
	shift

	command=$1
	shift

	if [ "$nflag" = "on" ]; then
		# don't execute command, just echo it
		echo
		if [ "$redirect" = "/dev/stdout" ]; then
			if [ "$vflag" = "on" ]; then
				echo "+" $command "$@"
			else
				echo "+" $command "$@" "> /dev/null"
			fi
		elif [ "$redirect" != "no" ]; then
			echo "+" $command "$@" "> $redirect"
		else
			echo "+" $command "$@"
		fi

	elif [ "$vflag" = "on" ]; then
		echo

		if [ "$redirect" = "/dev/stdout" ]; then
			set -x #echo on
			$command "$@"
			returnValue=$?
			set +x #echo off
		elif [ "$redirect" != "no" ]; then
			set -x #echo on
			$command "$@" > $redirect
			returnValue=$?
			set +x #echo off
		else
			set -x #echo on
			$command "$@"
			returnValue=$?
			set +x #echo off
		fi

		if [[ $returnValue != 0 && $returnValue != 5 ]] ; then
			stopProgress
			echo "ERROR - Command '$command $@' failed with error code: $returnValue"
			exit $returnValue
		fi
	else

		if [ "$redirect" = "/dev/stdout" ]; then
			$command "$@" > /dev/null
		elif [ "$redirect" != "no" ]; then
			$command "$@" > $redirect
		else
			$command "$@"
		fi

        returnValue=$?
		if [[ $returnValue != 0 && $returnValue != 5 ]] ; then
			stopProgress
			echo "ERROR - Command '$command $@' failed with error code: $returnValue"
			exit $returnValue
		fi


		echo
	fi
}

function convert_file {
  local xccovarchive_file="$1"
  local file_name="$2"
  local xccov_options="$3"
  echo "  <file path=\"$file_name\">"
  xcrun xccov view $xccov_options --file "$file_name" "$xccovarchive_file" | \
    sed -n '
    s/^ *\([0-9][0-9]*\): 0.*$/    <lineToCover lineNumber="\1" covered="false"\/>/p;
    s/^ *\([0-9][0-9]*\): [1-9].*$/    <lineToCover lineNumber="\1" covered="true"\/>/p
    '
  echo '  </file>'
}

function xccov_to_generic {
  echo '<coverage version="1">'
  local xccovarchive_file="$@"
  if [[ ! -d $xccovarchive_file ]]
  then
    echo "Coverage FILE NOT FOUND AT PATH: $xccovarchive_file" 1>&2;
    exit 1
  fi

  if [ $sdk_version -gt 10 ]; then # Apply optimization
    xccovarchive_file=$(optimize_format)
  fi

  local xccov_options=""
  if [[ $xccovarchive_file == *".xcresult"* ]]; then
    xccov_options="--archive"
  fi
  xcrun xccov view $xccov_options --file-list "$xccovarchive_file" | while read -r file_name; do
    convert_file "$xccovarchive_file" "$file_name" "$xccov_options"
  done
  echo '</coverage>'
}

function check_sdk_version {
  sdk_major_version=`xcrun --show-sdk-version | cut -d . -f 1`

  if [ $? -ne 0 ]; then 
    echo 'Failed to execute xcrun show-sdk-version' 1>&2
    exit -1
  fi
  echo $sdk_major_version
}

function cleanup_tmp_files {
  rm -rf tmp.json
  rm -rf tmp.xccovarchive
}

# Optimize coverage files conversion time by exporting to a clean xcodearchive directory
# Credits to silverhammermba on issue #68 for the suggestion
function optimize_format {
  cleanup_tmp_files
  xcrun xcresulttool get --format json --path "$xccovarchive_file" > tmp.json
  if [ $? -ne 0 ]; then 
    echo 'Failed to execute xcrun xcresulttool get' 1>&2
    exit -1
  fi

  # local reference=$(jq -r '.actions._values[2].actionResult.coverage.archiveRef.id._value'  tmp.json)
  local reference=$(jq -r '.actions._values[]|[.actionResult.coverage.archiveRef.id],._values'  tmp.json | grep value | cut -d : -f 2 | cut -d \" -f 2)
  if [ $? -ne 0 ]; then 
    echo 'Failed to execute jq (https://stedolan.github.io/jq/)' 1>&2
    exit -1
  fi
  # $reference can be a list of IDs (from a merged .xcresult bundle of multiple test plans)
  for test_ref in $reference; do
    xcrun xcresulttool export --type directory --path "$xccovarchive_file" --id "$test_ref" --output-path tmp.xccovarchive
    if [ $? -ne 0 ]; then 
      echo "Failed to execute xcrun xcresulttool export for reference ${test_ref}" 1>&2
      exit -1
    fi
  done
  echo "tmp.xccovarchive"
}

## COMMAND LINE OPTIONS
vflag="on"
nflag=""
unittests="${run_tests}"
swiftlint="${run_swiftlint}"
tailor="on"
lizard="on"
oclint="${run_oclint}"
dependencycheck="${run_dependency_check}"
sonarscanner="on"
enableDebug="${enable_detailed_log}"

# Usage OK
echo "Running run-sonar-swift.sh..."

#.xcodeproj filename
projectFile="${xcode_project}"
workspaceFile="${xcode_workspace}"

# Count projects
if [[ ! -z "$projectFile" ]]; then
	projectCount=$(echo $projectFile | sed -n 1'p' | tr ',' '\n' | wc -l | tr -d '[[:space:]]')
	if [ "$vflag" = "on" ]; then
	    echo "Project count is [$projectCount]"
	fi
fi

# Source directories for .swift files
srcDirs='./';
# The name of your application scheme in Xcode
appScheme="${app_scheme}"
# The app configuration to use for the build
appConfiguration=''
# The name of your test scheme in Xcode
testScheme="${tests_scheme}"
# The name of your binary file (application)
binaryName="${tests_binary_name}"

# Read destination simulator
destinationSimulator="${tests_simulator}"

# Read tailor configuration
tailorConfiguration=''

# Check for mandatory parameters
if [ "$unittests" = "on" ]; then
    if [ -z "$destinationSimulator" -o "$destinationSimulator" = " " ]; then
	      echo >&2 "ERROR - You must specify which simulator to use for unit tests."
	      exit 1
    fi
fi

# if the appConfiguration is not specified then set to Debug
if [ -z "$appConfiguration" -o "$appConfiguration" = " " ]; then
	appConfiguration="Debug"
fi

if [ "$vflag" = "on" ]; then
 	echo "Xcode project file is: $projectFile"
	echo "Xcode workspace file is: $workspaceFile"
 	echo "Xcode application scheme is: $appScheme"
  if [ -n "$unittests" ]; then
 	    echo "Destination simulator is: $destinationSimulator"
  else
      echo "Unit surefire are disabled"
  fi
fi

## SCRIPT

# Start progress indicator in the background
if [ "$vflag" = "" -a "$nflag" = "" ]; then
	startProgress &
	# Save PID
	PROGRESS_PID=$!
fi

# Create sonar-reports/ for reports output
if [ "$vflag" = "on" ]; then
    echo 'Creating directory sonar-reports/'
fi
rm -rf sonar-reports
mkdir sonar-reports

# Extracting project information needed later
echo -n 'Extracting Xcode project information'
if [[ "$workspaceFile" != "" ]] ; then
    buildCmdPrefix="-workspace $workspaceFile"
else
    buildCmdPrefix="-project $projectFile"
fi
buildCmd=($XCODEBUILD_CMD -skipPackagePluginValidation clean build $buildCmdPrefix -scheme "$appScheme")
if [[ ! -z "$destinationSimulator" ]]; then
    buildCmd+=(-destination "$destinationSimulator" -destination-timeout 360 COMPILER_INDEX_STORE_ENABLE=NO)
fi
runCommand  xcodebuild.log "${buildCmd[@]}"
#oclint-xcodebuild # Transform the xcodebuild.log file into a compile_command.json file
cat xcodebuild.log | $XCPRETTY_CMD -r json-compilation-database -o compile_commands.json

# Extract version
projet_version=`$XCODEBUILD_CMD $buildCmdPrefix -showBuildSettings | grep MARKETING_VERSION | tr -d 'MARKETING_VERSION ='`

# Objective-C code detection
hasObjC="no"
compileCmdFile=compile_commands.json
minimumSize=3
actualSize=$(stat -f%z "$compileCmdFile")
echo "actual = $actualSize, min = $minimumSize"
if [ $actualSize -ge $minimumSize ]; then
    hasObjC="yes"
fi

# Unit surefire and coverage
if [ "$unittests" = "on" ]; then
	runCommand sonar-reports/sonarqube-generic-coverage.xml xccov_to_generic "${BITRISE_XCRESULT_PATH}"
fi

# SwiftLint
if [ "$swiftlint" = "on" ]; then
	if hash $SWIFTLINT_CMD 2>/dev/null; then
		echo -n 'Running SwiftLint...'

		# Build the --include flags
		# Run SwiftLint command
		$SWIFTLINT_CMD lint > sonar-reports/"$appScheme"-swiftlint.txt
	else
		echo "Skipping SwiftLint (not installed!)"
	fi

else
	echo 'Skipping SwiftLint (test purposes only!)'
fi

if [ "$oclint" = "on" ] && [ "$hasObjC" = "yes" ]; then

	echo -n 'Running OCLint...'

	# Options
	maxPriority=10000
    longLineThreshold=250

	# Build the --include flags
	currentDirectory=${PWD##*/}
	echo "$srcDirs" | sed -n 1'p' | tr ',' '\n' > tmpFileRunSonarSh
	while read word; do

		includedCommandLineFlags=" --include .*/${currentDirectory}/${word}/*"
		if [ "$vflag" = "on" ]; then
            echo
            echo -n "Path included in oclint analysis is:$includedCommandLineFlags"
        fi
		# Run OCLint with the right set of compiler options
	    runCommand no oclint-json-compilation-database -v $includedCommandLineFlags -- -rc LONG_LINE=$longLineThreshold -max-priority-1 $maxPriority -max-priority-2 $maxPriority -max-priority-3 $maxPriority -report-type pmd -o sonar-reports/$appScheme-oclint.xml

	done < tmpFileRunSonarSh
	rm -rf tmpFileRunSonarSh


else
	echo 'Skipping OCLint (test purposes only!)'
fi

# SonarQube
if [ "$enableDebug" = "on"]; then
    sonarScannerOptions="-X "
fi

sonarScannerOptions="-Dsonar.host.url=${sonar_host_url} -Dsonar.login=${SONAR_HOST_LOGIN} -Dsonar.projectKey=${project_key} -Dsonar.language=swift -Dsonar.exclusions=${exclusions} -Dsonar.organization=${sonar_host_organization} -Dsonar.projectVersion=${projet_version}"

if [ "$unittests" = "on" ]; then
	sonarScannerOptions+=" -Dsonar.coverageReportPaths=sonar-reports/sonarqube-generic-coverage.xml"
	if [[ ! -z "${tests_exclusions}" ]]; then
		sonarScannerOptions+=" -Dsonar.coverage.exclusions=${tests_exclusions}"
	fi
fi

if [ "$dependencycheck" = "on" ]; then
	sonarScannerOptions+=" -Dsonar.dependencyCheck.jsonReportPath=${workspaceFile}/../dependency-check-report.json"
fi

if [ -z "$BITRISE_PULL_REQUEST" ]; then
  echo "Switching to Single Branch mode"
  echo "- Branch Name: ${BITRISE_GIT_BRANCH}"
  sonarScannerOptions+=" -Dsonar.branch.name=${BITRISE_GIT_BRANCH}"
else 
echo "Switching to Pull Request mode"
  echo "- Pull Request Branch: ${BITRISE_GIT_BRANCH}"
  echo "- Pull Request Key: ${BITRISE_PULL_REQUEST}"
  echo "- Pull Request Base: ${BITRISE_GIT_BRANCH_DEST}"
  sonarScannerOptions+=" -Dsonar.pullrequest.branch=${BITRISE_GIT_BRANCH} -Dsonar.pullrequest.key=${BITRISE_PULL_REQUEST} -Dsonar.pullrequest.base=${BITRISEIO_GIT_BRANCH_DEST}"
fi

if [ -z $extras ]; then 
    echo -n 'No extra parameter provided'
else 
    echo -n "Adding extra parameters: $extras"
    sonarScannerOptions+=" ${extras}"
fi

if [ "$sonarscanner" = "on" ]; then
    echo -n 'Running SonarQube using SonarQube Scanner'
    if hash /dev/stdout sonar-scanner 2>/dev/null; then
		runCommand /dev/stdout sonar-scanner $sonarScannerOptions
    else
        echo 'Skipping sonar-scanner (not installed!)'
    fi
else
    echo -n 'Running SonarQube using SonarQube Runner'
    if hash /dev/stdout sonar-runner 2>/dev/null; then
	   runCommand /dev/stdout sonar-runner $sonarScannerOptions
    else
	   runCommand /dev/stdout sonar-scanner $sonarScannerOptions
    fi
fi

# Kill progress indicator
stopProgress

#
# --- Exit codes:
# The exit code of your Step is very important. If you return
#  with a 0 exit code `bitrise` will register your Step as "successful".
# Any non zero exit code will be registered as "failed" by `bitrise`.
exit 0
