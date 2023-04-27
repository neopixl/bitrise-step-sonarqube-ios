import os

print("\n\n\n\n\n* * * * * * * *      STARTING NEOPIXL SONAR SCRIPT       * * * * * * * * * \n\n\n\n\n", flush=True)

# Install all dependencies
print("\n\n\n\n\n* * * * * * * *      Install all dependencies       * * * * * * * * * \n", flush=True)

os.system("pip3 install mobsfscan");

project_root_path = "/Users/vagrant/git" #"/Users/joris/Documents/Neopixl/Apps/Visa-iOS" #

# Retrieve all user injected variables
print("\n\n\n\n\n* * * * * * * *      Retrieve all user injected variables       * * * * * * * * * \n", flush=True)

sonar_project_name = "visa-ios"
xcodeproj_path = "%s/Visa.xcodeproj" % project_root_path
xcworkspace_path = ""
scheme = "Visa-env_DEV"
sonar_host_url = "https://sonar.smile.fr"
sonar_login = "a94185abb45a1db7dd9f2f14d101a6eaf0b7b9c0"

print("	    sonar project name 		= %s" % sonar_project_name, flush=True)
print("	    project_root_path 		= %s" % project_root_path, flush=True)
print("	    xcodeproj_path 			= %s" % xcodeproj_path, flush=True)
print("	    xcworkspace_path 		= %s" % xcworkspace_path, flush=True)
print("	    scheme 					= %s" % scheme, flush=True)
print("	    sonar_host_url 			= %s" % sonar_host_url, flush=True)

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
#os.system("xcodebuild -resolvePackageDependencies"); #generate spm package.resolved used for dependency check TODO: need that ?
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
print("cmd sonar-scanner === %s" % sonar_scanner_cmd, flush=True)
os.system(sonar_scanner_cmd);


print("\n\n\n\n\n* * * * * * * *      FINISHING NEOPIXL SONAR SCRIPT       * * * * * * * * * \n", flush=True)

