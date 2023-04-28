import os
import sys

print("\n\n\n\n\n* * * * * * * *      STARTING NEOPIXL SONAR SCRIPT       * * * * * * * * * \n\n\n\n\n", flush=True)

TEST1 = os.getenv('xcode_project_path')
TEST2 = os.getenv('${xcode_project_path}')
TEST3 = os.getenv('$xcode_project_path')

print("_____________TTTTTTTTTTTTTEST_1111 = %s" % TEST1)
print("_____________TTTTTTTTTTTTTEST_2222 = %s" % TEST2)
print("_____________TTTTTTTTTTTTTEST_2222 = %s" % TEST3)

# Install all dependencies
print("\n\n\n\n\n* * * * * * * *      Install all needed dependencies       * * * * * * * * * \n", flush=True)

os.system("pip3 install mobsfscan");

project_root_path = "/Users/vagrant/git"

# Retrieve all user injected variables
print("\n\n\n\n\n* * * * * * * *      Retrieve all user injected variables       * * * * * * * * * \n", flush=True)

xcodeproj_path = "%s/%s" % (project_root_path, sys.argv[1])
xcworkspace_path = "%s/%s" % (project_root_path, sys.argv[2])
scheme = sys.argv[3]
sonar_project_name = sys.argv[4]
sonar_host_url = sys.argv[5]
sonar_login = sys.argv[6]

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

