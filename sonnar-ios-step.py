import os
import json
import subprocess

print("""\n\n\n
███╗   ██╗███████╗ ██████╗ ██████╗ ██╗██╗  ██╗██╗         ███████╗ ██████╗ ███╗   ██╗ █████╗ ██████╗     ███████╗████████╗███████╗██████╗ 
████╗  ██║██╔════╝██╔═══██╗██╔══██╗██║╚██╗██╔╝██║         ██╔════╝██╔═══██╗████╗  ██║██╔══██╗██╔══██╗    ██╔════╝╚══██╔══╝██╔════╝██╔══██╗
██╔██╗ ██║█████╗  ██║   ██║██████╔╝██║ ╚███╔╝ ██║         ███████╗██║   ██║██╔██╗ ██║███████║██████╔╝    ███████╗   ██║   █████╗  ██████╔╝
██║╚██╗██║██╔══╝  ██║   ██║██╔═══╝ ██║ ██╔██╗ ██║         ╚════██║██║   ██║██║╚██╗██║██╔══██║██╔══██╗    ╚════██║   ██║   ██╔══╝  ██╔═══╝ 
██║ ╚████║███████╗╚██████╔╝██║     ██║██╔╝ ██╗███████╗    ███████║╚██████╔╝██║ ╚████║██║  ██║██║  ██║    ███████║   ██║   ███████╗██║     
╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝    ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚══════╝   ╚═╝   ╚══════╝╚═╝                                                                                                                                                                                                                    
\n""", flush=True)

project_root_path = "/Users/vagrant/git"

# Install all dependencies
print("""\n
 ___                                    __  _ 
  |  ._   _ _|_  _. | |   | /|  _  |_  (_  |_ 
 _|_ | | _>  |_ (_| | |   |  | (_) |_) __) |
\n""", flush=True)


exit_code = os.system("pip3 install mobsfscan --break-system-packages --quiet")
print("\n exit_code : instalMobsf === %s" % exit_code, flush=True)
if exit_code != 0:
    exit_func = "exit %d" % exit_code
    os.system(exit_func)

os.system("mobsfscan --v");


# Retrieve all user injected variables
print("""\n\n
 ___                                                          
  |  ._  o  _   _ _|_  _   _|      / _. ._ o  _. |_  |  _   _ 
 _|_ | | | (/_ (_  |_ (/_ (_|     / (_| |  | (_| |_) | (/_ _> 
        _|
 \n""", flush=True)

#project configuration
print("\n----> Add project configuration\n", flush=True)
xcodeproj_path = "%s/%s" % (project_root_path, os.getenv('xcode_project_path'))

xcworkspace_path = ""
if os.getenv('xcode_workspace_path') != "":
	xcworkspace_path = "%s/%s" % (project_root_path, os.getenv('xcode_workspace_path')) 

podfile_path = ""
if os.getenv('podfile_path') != "":
	podfile_path = "%s/%s" % (project_root_path, os.getenv('podfile_path')) 

scheme = os.getenv('app_scheme')

print("\n xcodeproj_path === %s" % xcodeproj_path)
print("\n xcworkspace_path === %s" % xcworkspace_path)
print("\n podfile_path === %s" % podfile_path)
print("\n scheme === %s" % scheme)

#sonar server configuration
print("\n----> Add Sonar server configuration\n", flush=True)
sonar_project_name = os.getenv('sonar_project_key')
sonar_host_url = os.getenv('sonar_host_url')
sonar_login = os.getenv('sonar_login')
sonar_branch = os.getenv('BITRISE_GIT_BRANCH')

print("\n sonar_project_name === %s" % sonar_project_name)
print("\n sonar_host_url === %s" % sonar_host_url)
print("\n sonar_login === %s" % sonar_login)
print("\n sonar_branch === %s" % sonar_branch)

#other configuration
print("\n----> Add other configuration\n", flush=True)
verbose_mode_enabled = os.getenv('verbose_mode_enabled')
exclusion_file = os.getenv('exclusion_file')
run_unit_test = os.getenv('run_unit_test')
run_dcheck = os.getenv('run_dcheck')
run_dtrack = os.getenv('run_dtrack')
run_periphery = os.getenv('run_periphery')
target_name = os.getenv('target_name')
extra_sonar_param = os.getenv('extra_sonar_param')
nvd_api_key = os.getenv('nvd_api_key')

print("\n verbose_mode_enabled === %s" % verbose_mode_enabled)
print("\n exclusion_file === %s" % exclusion_file)
print("\n run_unit_test === %s" % run_unit_test)
print("\n run_dcheck === %s" % run_dcheck)
print("\n run_dtrack === %s" % run_dtrack)
print("\n run_periphery === %s" % run_periphery)
print("\n target_name === %s" % target_name)
print("\n extra_sonar_param === %s" % extra_sonar_param)
print("\n nvd_api_key === %s" % nvd_api_key)

# Build project
print("""\n\n
  _                 _                     
 |_)     o |  _|   |_) ._ _  o  _   _ _|_ 
 |_) |_| | | (_|   |   | (_) | (/_ (_  |_ 
                            _|
\n""", flush=True)

print("\n  ----> Build the project (to generate derived data files & xcresult) \n", flush=True)
xcodebuild_cmd = "xcrun xcodebuild "
xcodebuild_cmd += "-project %s " % xcodeproj_path
xcodebuild_cmd += "-scheme %s " % scheme
#xcodebuild_cmd += "-sdk iphonesimulator "
xcodebuild_cmd += "-destination 'platform=iOS Simulator,name=iPhone 15,OS=latest' "
xcodebuild_cmd += "-resultBundlePath 'build/result.xcresult' "
xcodebuild_cmd += "-derivedDataPath '/Users/vagrant/derivedData' "

if run_unit_test == "on":
    xcodebuild_cmd += "clean test"

if verbose_mode_enabled != 'on':
    xcodebuild_cmd += " > /dev/null"

print("\n xcodebuild_cmd === %s" % xcodebuild_cmd)
exit_code = os.system(xcodebuild_cmd);

print("\n exit_code : XcodeBuild === %s" % exit_code, flush=True)

exit_code = 333
if exit_code != 0:
    exit_func = "exit %d" % exit_code
    print("\n exit_func : exit_func === %s" % exit_func, flush=True)
    os.system("exit 2")

# Prepare sonar-scanner options
print("""\n\n
  __                   _                      
 (_   _  ._   _. ._   /   ._ _|_ o  _  ._   _ 
 __) (_) | | (_| |      / |_) |_ | (_) | | _> 
                          |
\n""", flush=True)
sonar_scanner_cmd = "sonar-scanner "

# Authentification to sonar
print("\n-> Add authentification to sonar options\n", flush=True)
sonar_scanner_cmd += "-Dsonar.host.url=%s " % sonar_host_url
sonar_scanner_cmd += "-Dsonar.login=%s " % sonar_login

# Project settings & config
print("\n-> Add project config to sonar options\n", flush=True)
sonar_scanner_cmd += "-Dsonar.apple.project=%s " % xcodeproj_path

if xcworkspace_path != "":
	sonar_scanner_cmd += "-Dsonar.apple.workspace=%s " % xcworkspace_path

sonar_scanner_cmd += "-Dsonar.projectKey=%s " % sonar_project_name
sonar_scanner_cmd += "-Dsonar.exclusions=%s " % exclusion_file
sonar_scanner_cmd += "-Dsonar.sources='%s' " % project_root_path
sonar_scanner_cmd += "-Dsonar.branch.name='%s' " % sonar_branch

#Get version
print("\n-> Get Project Version \n", flush=True)
projet_version_cmd = "xcodebuild clean -showBuildSettings | grep MARKETING_VERSION | tr -d 'MARKETING_VERSION ='"
projet_version = os.popen(projet_version_cmd).read()
projet_version = projet_version.replace('\n', '')
projet_version = projet_version.replace('\r', '')
projet_version = projet_version.replace('\b', '')
projet_version = projet_version.replace('\n', '')
print("\n  -> Project Version: %s \n" % projet_version, flush=True)
sonar_scanner_cmd += "-Dsonar.projectVersion=%s " % projet_version

# Unit test
if run_unit_test == "on":
    print("\n-> Setup unit test in sonar cmd \n", flush=True)
    sonar_scanner_cmd += "-Dsonar.apple.resultBundlePath=build/result.xcresult "

# Dependency Check (security hotspot)
if run_dcheck == "on":
    print("\n-> Add Dependency-check to sonar options \n", flush=True)

    pod_scan_option = ""
    spm_scan_option = ""

    is_SPM_Exist = os.path.exists("%s/project.xcworkspace/xcshareddata/swiftpm/Package.resolved" % xcodeproj_path) 
    print("\n-> SPM (Package.resolved) file exist : %s \n" % is_SPM_Exist, flush=True)

    if is_SPM_Exist == True:
        spm_scan_option = "--scan %s/project.xcworkspace/xcshareddata/swiftpm/Package.resolved" % xcodeproj_path

    if podfile_path != "":
        pod_scan_option = "--scan %s" % podfile_path

    dep_check_cmd = "dependency-check --enableExperimental --project %s --nvdApiKey %s --format JSON --format HTML %s %s --data %s" % (xcodeproj_path, nvd_api_key, spm_scan_option, pod_scan_option, "/Users/vagrant/DependencyCheckCVECacheDB")
    print("\n-> Launch Dependency-check (to generate report file) cmd %s\n" % dep_check_cmd, flush=True)
    exit_code = os.system(dep_check_cmd);
    print("\n exit_code : depcheck === %s" % exit_code, flush=True)

    sonar_scanner_cmd += "-Dsonar.dependencyCheck.jsonReportPath=%s/%s " % (project_root_path, "dependency-check-report.json")
    sonar_scanner_cmd += "-Dsonar.dependencyCheck.htmlReportPath=%s/%s " % (project_root_path, "dependency-check-report.html")
    sonar_scanner_cmd += "-Dsonar.dependencyCheck.summarize=true "
    sonar_scanner_cmd += "-Dsonar.dependencyCheck.securityHotspot=true "

# Periphery (code duplication & dead code)
if run_periphery == "on":
    print("\n-> Launch Periphery (code duplication & dead code)\n", flush=True)

    sonar_scanner_cmd += "-Dsonar.apple.periphery.schemes=%s " % scheme
    sonar_scanner_cmd += "-Dsonar.apple.periphery.indexStorePath=%s " % "'/Users/vagrant/derivedData/Index.noindex/DataStore'"
    sonar_scanner_cmd += "-Dsonar.apple.periphery.targets=%s " % target_name

# Verbose
if verbose_mode_enabled == 'on':
    sonar_scanner_cmd += "-X -Dsonar.verbose=true "

# Extra sonar scanner parameters (if any)
sonar_scanner_cmd += "%s" % extra_sonar_param

print("""\n\n
  _             __                   _       _  
 |_)     ._    (_   _  ._   _. ._   /  | /| | \
 |  |_| | |   __) (_) | | (_| |      |  | |_/
 \n""", flush=True)

print("\n----> Final cmd sonar-scanner == %s\n\n" % sonar_scanner_cmd, flush=True)
exit_code = os.system(sonar_scanner_cmd);

print("\n exit_code : sonar-scanner === %s" % exit_code, flush=True)


# Dependency Track (third party libraries)
if run_dtrack == "on":
    print("""\n\n
      _____                            _                         _______             _    
     |  __                            | |                       |__   __|           | |   
     | |  | | ___ _ __   ___ _ __   __| | ___ _ __   ___ _   _     | |_ __ __ _  ___| | __
     | |  | |/ _   '_   / _   '_   / _` |/ _   '_   / __| | | |    | | '__/ _` |/ __| |/ /
     | |__| |  __/ |_) |  __/ | | | (_| |  __/ | | | (__| |_| |    | | | | (_| | (__|   < 
     |_____/  ___| .__/  ___|_| |_| __,_| ___|_| |_| ___| __, |    |_|_|   __,_|__ _|_| _\
                 | |                                      __/ |                           
                 |_|                                     |___/                            

     \n""", flush=True)

    # Retrieve Package.resolved and transform it to bom.json
    package_path = "%s/project.xcworkspace/xcshareddata/swiftpm/Package.resolved" % xcodeproj_path

    print("read package at path : %s" % package_path, flush=True)

    components = []
    package_json = open(package_path)
    data = json.load(package_json)
    for i in data['pins']:

        #generate purl
        purl = i['identity']
        purl += "@"
        purl += i['state']['version']

        #generate CPE (vulnerabilities) thanks to DCheck report..."
        dcheck_report_json = open("dependency-check-report.json") 
        dcheck_report_data = json.load(dcheck_report_json)

        cpe_id = "none"

        for f in dcheck_report_data['dependencies']:
            filenameArray = f['fileName'].split(":")
            if filenameArray[0] == i['identity']:
                if not (f.get('vulnerabilityIds') is None):
                    cpe_id = f['vulnerabilityIds'][0]['id']
        
        externalReferences = [{"url": i['location'], "type": "vcs"}]

        package_dict = {
        "type": "library",
        "name": i['identity'],
        "version": i['state']['version'],
        "purl": purl,
        "cpe": cpe_id,
        "externalReferences": externalReferences
        }

        components.append(package_dict)

    package_json.close()

    sbom_dict = {
        "bomFormat": "CycloneDX",
        "version": 1,
        "specVersion": "1.5",
        "components": components
    }

    print("\n-> generated sbom = %s\n" % sbom_dict, flush=True)

    # send sbom to dtrack
    headers = {
        'Content-Type': 'multipart/form-data',
        'X-Api-Key': 'dtrackAPIKey'
    }
    files = {
        'autoCreate': (None, 'true'),
        'projectName': (None, os.getenv('project_key', '')),
        'projectVersion': (None, os.getenv('projet_version', ''))
    }
    #response = requests.post('$dtrackBaseUrl/api/v1/bom', json=sbom_dict, headers=headers, files=files)

print("""\n\n
███████╗███╗   ██╗██████╗ 
██╔════╝████╗  ██║██╔══██╗
█████╗  ██╔██╗ ██║██║  ██║
██╔══╝  ██║╚██╗██║██║  ██║
███████╗██║ ╚████║██████╔╝
╚══════╝╚═╝  ╚═══╝╚═════╝ 
\n""", flush=True)

