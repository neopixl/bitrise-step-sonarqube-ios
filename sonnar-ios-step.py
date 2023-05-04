import os

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
  |  ._   _ _|_  _. | |   |\/|  _  |_  (_  |_ 
 _|_ | | _>  |_ (_| | |   |  | (_) |_) __) |
\n""", flush=True)

os.system("pip3 install mobsfscan --quiet");

print("\n-> MobSF installed\n", flush=True)

# Retrieve all user injected variables
print("""\n\n
 ___                                                          
  |  ._  o  _   _ _|_  _   _|   \  / _. ._ o  _. |_  |  _   _ 
 _|_ | | | (/_ (_  |_ (/_ (_|    \/ (_| |  | (_| |_) | (/_ _> 
        _|
 \n""", flush=True)

#project configuration
print("\n-> Add project configuration\n", flush=True)
xcodeproj_path = "%s/%s" % (project_root_path, os.getenv('xcode_project_path'))

xcworkspace_path = ""
if os.getenv('xcode_workspace_path') != "":
	xcworkspace_path = "%s/%s" % (project_root_path, os.getenv('xcode_workspace_path')) 

podfile_path = ""
if os.getenv('podfile_path') != "":
	podfile_path = "%s/%s" % (project_root_path, os.getenv('podfile_path')) 

scheme = os.getenv('app_scheme')

#sonar server configuration
print("\n-> Add Sonar server configuration\n", flush=True)
sonar_project_name = os.getenv('sonar_project_key')
sonar_host_url = os.getenv('sonar_host_url')
sonar_login = os.getenv('sonar_login')

#other configuration
print("\n-> Add other configuration\n", flush=True)
verbose_mode_enabled = os.getenv('verbose_mode_enabled')
exclusion_file = os.getenv('exclusion_file')
run_unit_test = os.getenv('run_unit_test')

# Prepare sonar-scanner options
print("""\n\n
  __                   _                      
 (_   _  ._   _. ._   / \ ._ _|_ o  _  ._   _ 
 __) (_) | | (_| |    \_/ |_) |_ | (_) | | _> 
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

# Dependency Check (security hotspot)
print("\n-> Add Dependency-check to sonar options \n", flush=True)

pod_scan_option = ""
spm_scan_option = ""

is_SPM_Exist = os.path.exists("%s/project.xcworkspace/xcshareddata/swiftpm/Package.resolved" % xcodeproj_path) 
print("\n-> SPM (Package.resolved) file exist : %s \n" % is_SPM_Exist, flush=True)

if is_SPM_Exist == "True":
	spm_scan_option = "--scan %s/project.xcworkspace/xcshareddata/swiftpm/Package.resolved" % xcodeproj_path

if podfile_path != "":
	pod_scan_option = "--scan %s" % podfile_path

dep_check_cmd = "dependency-check --enableExperimental --project %s --format JSON --format HTML %s %s" % (xcodeproj_path, spm_scan_option, pod_scan_option)
print("\n-> Launch Dependency-check cmd %s\n" % dep_check_cmd, flush=True)
os.system(dep_check_cmd);
sonar_scanner_cmd += "-Dsonar.dependencyCheck.jsonReportPath=%s/%s " % (project_root_path, "dependency-check-report.json")
sonar_scanner_cmd += "-Dsonar.dependencyCheck.htmlReportPath=%s/%s " % (project_root_path, "dependency-check-report.html")
sonar_scanner_cmd += "-Dsonar.dependencyCheck.summarize=true "
sonar_scanner_cmd += "-Dsonar.dependencyCheck.securityHotspot=true "

# Periphery (code duplication & dead code)
print("\n-> Launch Periphery (code duplication & dead code)\n", flush=True)
sonar_scanner_cmd += "-Dsonar.apple.periphery.schemes=%s " % scheme
sonar_scanner_cmd += "-Dsonar.apple.periphery.indexStorePath=%s " % "derivedData/Index/DataStore"
sonar_scanner_cmd += "-Dsonar.apple.periphery.targets=%s " % "MyiOSAppTarget"

#Get version
print("\n-> Get Project Version \n", flush=True)
projet_version_cmd = "xcodebuild clean -showBuildSetting"# | grep MARKETING_VERSION | tr -d 'MARKETING_VERSION ='"
projet_version = os.popen(projet_version_cmd).read()
print("TESTEST : %s" % projet_version, flush=True)
sonar_scanner_cmd += "-Dsonar.projectVersion=%s " % projet_version



# Unit test
if run_unit_test == "on":
    print("\n-> Run unit test \n", flush=True)
    print("\n    -> First, build the project \n", flush=True)
    xcodebuild_cmd = "xcrun xcodebuild "
    xcodebuild_cmd += "-project %s " % xcodeproj_path
    xcodebuild_cmd += "-scheme %s " % scheme
    xcodebuild_cmd += "-sdk iphonesimulator "
    xcodebuild_cmd += "-destination 'platform=iOS Simulator,name=iPhone 14 Plus' "
    xcodebuild_cmd += "-derivedDataPath './derivedData' "
    xcodebuild_cmd += "-resultBundlePath 'build/result.xcresult' "
    xcodebuild_cmd += "-quiet "
    xcodebuild_cmd += "clean test"
    print("xcodebuild_cmd === %s" % xcodebuild_cmd)
    #sonar.apple.resultBundlePath=custom/path/to/file.xcresult # Defaults to build/result.xcresult
    os.system(xcodebuild_cmd);

# Verbose
print("""\n\n
  _             __                   _       _  
 |_)     ._    (_   _  ._   _. ._   /  |\/| | \ 
 | \ |_| | |   __) (_) | | (_| |    \_ |  | |_/
 \n""", flush=True)
if verbose_mode_enabled == 'on':
	sonar_scanner_cmd += "-X -Dsonar.verbose=true "

print("\n-> Final cmd sonar-scanner == %s\n\n" % sonar_scanner_cmd, flush=True)
os.system(sonar_scanner_cmd);


print("""\n\n
███████╗███╗   ██╗██████╗ 
██╔════╝████╗  ██║██╔══██╗
█████╗  ██╔██╗ ██║██║  ██║
██╔══╝  ██║╚██╗██║██║  ██║
███████╗██║ ╚████║██████╔╝
╚══════╝╚═╝  ╚═══╝╚═════╝ 
\n""", flush=True)

