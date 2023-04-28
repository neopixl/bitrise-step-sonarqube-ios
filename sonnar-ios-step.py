import os

print("\n\n\n\n\n* * * * * * * *      STARTING NEOPIXL SONAR SCRIPT       * * * * * * * * * \n\n\n\n\n", flush=True)

# Install all dependencies
print("\n\n\n\n\n* * * * * * * *      Install all needed dependencies       * * * * * * * * * \n", flush=True)

os.system("pip3 install mobsfscan");

project_root_path = "/Users/vagrant/git"

# Retrieve all user injected variables
print("\n\n\n\n\n* * * * * * * *      Retrieve all user injected variables       * * * * * * * * * \n", flush=True)

xcodeproj_path = "%s/%s" % (project_root_path, os.getenv('xcode_project_path'))
xcworkspace_path = "%s/%s" % (project_root_path, os.getenv('xcode_workspace_path'))
scheme = os.getenv('app_scheme')
sonar_project_name = os.getenv('sonar_project_key')
sonar_host_url = os.getenv('sonar_host_url')
sonar_login = os.getenv('sonar_login')

print("\n\n\n\n\n* * * * * * * *   TEST_TEST_TEST %s %s \n",(xcodeproj_path, scheme))

# Prepare sonar-scanner options
print("\n\n\n\n\n* * * * * * * *      Prepare sonar-scanner options       * * * * * * * * * \n", flush=True)
sonar_scanner_cmd = "sonar-scanner "

# Authentification to sonar
print("\n\n\n\n\n* * * * * * * *      Add authentification to sonar options       * * * * * * * * * \n", flush=True)
sonar_scanner_cmd += "-Dsonar.host.url=%s " % sonar_host_url
sonar_scanner_cmd += "-Dsonar.login=%s " % sonar_login

# Project settings & config
print("\n\n\n\n\n* * * * * * * *      Add project config to sonar options       * * * * * * * * * \n", flush=True)
sonar_scanner_cmd += "-Dsonar.apple.project=%s " % xcodeproj_path
sonar_scanner_cmd += "-Dsonar.projectKey=%s " % sonar_project_name
sonar_scanner_cmd += "-Dsonar.exclusions=**/*.xml,Pods/**/*,Reports/**/*,**/SourcePackages/checkouts/**/*,**/*.html "
sonar_scanner_cmd += "-Dsonar.sources='%s' " % project_root_path

# Dependency Check (security hotspot)
print("\n\n\n\n\n* * * * * * * *      Add Dependency-check to sonar options       * * * * * * * * * \n", flush=True)
dep_check_cmd = "dependency-check --enableExperimental --project %s --format JSON --format HTML --scan %s/project.xcworkspace/xcshareddata/swiftpm/Package.resolved" % (xcodeproj_path, xcodeproj_path)
os.system(dep_check_cmd);
sonar_scanner_cmd += "-Dsonar.dependencyCheck.jsonReportPath=%s/%s " % (project_root_path, "dependency-check-report.json")
sonar_scanner_cmd += "-Dsonar.dependencyCheck.htmlReportPath=%s/%s " % (project_root_path, "dependency-check-report.html")
sonar_scanner_cmd += "-Dsonar.dependencyCheck.summarize=true "
sonar_scanner_cmd += "-Dsonar.dependencyCheck.securityHotspot=true "

# Verbose
print("\n\n\n\n\n* * * * * * * *      Verbose to sonar options       * * * * * * * * * \n", flush=True)
#sonar_scanner_cmd += "-X -Dsonar.verbose=true "

print("\n\n\n\n\n* * * * * * * *      RUN SONAR COMMAND       * * * * * * * * * \n", flush=True)
print("cmd sonar-scanner == %s" % sonar_scanner_cmd, flush=True)
os.system(sonar_scanner_cmd);


print("\n\n\n\n\n* * * * * * * *      FINISHING NEOPIXL SONAR SCRIPT       * * * * * * * * * \n", flush=True)

