#!/bin/bash
set -e

# Global parameters
SLATHER_CMD=slather
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

runCommand /dev/stdout curl -v "${SONAR_HOST_URL}"

## COMMAND LINE OPTIONS
vflag="on"
nflag=""
unittests="${run_tests}"
swiftlint="${run_swiftlint}"
tailor="on"
lizard="on"
oclint="${run_oclint}"
sonarscanner="on"

# Usage OK
echo "Running run-sonar-swift.sh..."

#.xcodeproj filename
projectFile="${BITRISE_PROJECT_PATH}"
workspaceFile="${BITRISE_WORKSPACE_PATH}"

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
appScheme="${BITRISE_SCHEME}"
# The app configuration to use for the build
appConfiguration=''
# The name of your test scheme in Xcode
testScheme="${tests_scheme}"
# The name of your binary file (application)
binaryName="${project_key}"
# Get the path of plist file
plistFile=`xcodebuild -showBuildSettings -project "${projectFile}" | grep -i 'PRODUCT_SETTINGS_PATH' -m 1 | sed 's/[ ]*PRODUCT_SETTINGS_PATH = //'`
# Number version from plist if no sonar.projectVersion
numVerionFromPlist=`defaults read ${plistFile} CFBundleShortVersionString`

# Read destination simulator
destinationSimulator="${tests_simulator}"

# Read tailor configuration
tailorConfiguration=''

# The file patterns to exclude from coverage report
excludedPathsFromCoverage=''

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
    echo "Number version from plist is: $numVerionFromPlist"
  if [ -n "$unittests" ]; then
 	    echo "Destination simulator is: $destinationSimulator"
 	    echo "Excluded paths from coverage are: $excludedPathsFromCoverage"
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
buildCmd=($XCODEBUILD_CMD clean build $buildCmdPrefix -scheme $appScheme)
if [[ ! -z "$destinationSimulator" ]]; then
    buildCmd+=(-destination "$destinationSimulator" -destination-timeout 360 COMPILER_INDEX_STORE_ENABLE=NO)
fi
runCommand  xcodebuild.log "${buildCmd[@]}"
#oclint-xcodebuild # Transform the xcodebuild.log file into a compile_command.json file
cat xcodebuild.log | $XCPRETTY_CMD -r json-compilation-database -o compile_commands.json

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

    # Put default xml files with no surefire and no coverage...
    echo "<?xml version='1.0' encoding='UTF-8' standalone='yes'?><testsuites name='AllTestUnits'></testsuites>" > sonar-reports/TEST-report.xml
    echo "<?xml version='1.0' ?><!DOCTYPE coverage SYSTEM 'http://cobertura.sourceforge.net/xml/coverage-03.dtd'><coverage><sources></sources><packages></packages></coverage>" > sonar-reports/coverage-swift.xml

    echo -n 'Running surefire'
    buildCmd=($XCODEBUILD_CMD clean build test)
    if [[ ! -z "$workspaceFile" ]]; then
        buildCmd+=(-workspace "$workspaceFile")
    elif [[ ! -z "$projectFile" ]]; then
	      buildCmd+=(-project "$projectFile")
    fi
    buildCmd+=( -scheme "$appScheme" -configuration "$appConfiguration" -enableCodeCoverage YES)
    if [[ ! -z "$destinationSimulator" ]]; then
        buildCmd+=(-destination "$destinationSimulator" -destination-timeout 60)
    fi

    runCommand  sonar-reports/xcodebuild.log "${buildCmd[@]}"
    cat sonar-reports/xcodebuild.log  | $XCPRETTY_CMD -t --report junit
    mv build/reports/junit.xml sonar-reports/TEST-report.xml


    echo '\nComputing coverage report\n'

    # Build the --exclude flags
    excludedCommandLineFlags=""
    if [ ! -z "$excludedPathsFromCoverage" -a "$excludedPathsFromCoverage" != " " ]; then
	      echo $excludedPathsFromCoverage | sed -n 1'p' | tr ',' '\n' > tmpFileRunSonarSh2
	      while read word; do
		        excludedCommandLineFlags+=" -i $word"
	      done < tmpFileRunSonarSh2
	      rm -rf tmpFileRunSonarSh2
    fi
    if [ "$vflag" = "on" ]; then
	      echo "Command line exclusion flags for slather is:$excludedCommandLineFlags"
    fi

	firstProject=$(echo $projectFile | sed -n 1'p' | tr ',' '\n' | head -n 1)

    slatherCmd=($SLATHER_CMD coverage)
    if [[ ! -z "$binaryName" ]]; then
    	slatherCmd+=( --binary-basename "$binaryName")
    fi

    slatherCmd+=( --input-format profdata $excludedCommandLineFlags --cobertura-xml --output-directory sonar-reports)

    if [[ ! -z "$workspaceFile" ]]; then
        slatherCmd+=( --workspace "$workspaceFile")
    fi
    slatherCmd+=( --scheme "$appScheme" "$firstProject")

    echo "${slatherCmd[@]}"

    runCommand /dev/stdout "${slatherCmd[@]}"
    mv sonar-reports/cobertura.xml sonar-reports/coverage-swift.xml
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
sonarScannerOptions="--verbose -Dsonar.host.url=${SONAR_HOST_URL} -Dsonar.login=${SONAR_HOST_LOGIN} -Dsonar.projectKey=$binaryName"
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