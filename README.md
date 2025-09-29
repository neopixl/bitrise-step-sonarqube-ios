# Bitrise Step - SonarQube iOS

[![Bitrise](https://img.shields.io/badge/Bitrise-Step-purple)](https://www.bitrise.io)
[![Platform](https://img.shields.io/badge/platform-iOS-lightgrey)](https://developer.apple.com/ios/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 📢 Introduction

A comprehensive Bitrise step for analyzing iOS code **quality and security** for sending results to **SonarQube**.

## 🎯 Features

This step automates code quality and security for iOS projects by combining multiple tools:

- **SonarQube Scanner**: Static analysis of Swift/Objective-C code quality (lint)
- **SwiftLint**: Static analysis of Swift/Objective-C code quality ([SwiftLint]https://github.com/realm/SwiftLint)
- **Periphery**: Dead code and code duplication detection ([Periphery](https://github.com/peripheryapp/periphery))
- **Dependency-Check**: Vulnerability detection in dependencies (CocoaPods & SPM) ([Dependency-Check](https://github.com/dependency-check/DependencyCheck))
- **MobSFScan**: Mobile security analysis ([MobSFScan](https://github.com/MobSF/mobsfscan))
- **Unit Tests**: Integration of test results with code coverage (from Xcode)
- **UI Tests**: Integration of UI test results with code coverage (from Xcode)
- **Dependency-Track** 🚧 Work In Progress 🚧

➜ The result of all these analyses are sended to SonarQube instance.

## 🚀 Installation

The prerequisite for this step is that plugin [sonar-apple](https://github.com/insideapp-oss/sonar-apple) is installed on the SonarQube instance.

1. Open your project on **Bitrise**
2. Go to the **Workflow Editor** tab
3. Click **Configuration YAML** to see yaml of your configuration
4. Add it to your **workflow**

```yaml
- git::https://github.com/neopixl/bitrise-step-sonarqube-ios.git@2.0:
    title: SonarQube iOS Analysis
    inputs:
    - xcode_project_path: "MyProject.xcodeproj"
    - app_scheme: "MyScheme"
    - target_name: "MyTarget"
    - sonar_project_key: "my-ios-project"
    - sonar_host_url: "https://sonarqube.mycompany.com"
    - sonar_login: "$SONAR_TOKEN"
    - nvd_api_key: "$NVD_API_KEY"
    - ...: ...
```

Don't forget to force the version of this step by using **@x.y** at the end of **- git::https://** command

## ⚙️ Configuration

### Adding Parameters

To set parameters for this step, just look at the step details (configuration) in Bitrise.

### Required Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `xcode_project_path` | Path to the `.xcodeproj` file | `MyApp.xcodeproj` |
| `app_scheme` | Xcode scheme name | `MyApp` |
| `target_name` | Main target name | `MyApp` |
| `sonar_project_key` | SonarQube project key | `com.company.myapp` |
| `sonar_host_url` | SonarQube server URL | `https://sonar.example.com` |
| `sonar_login` | SonarQube authentication token | `squ_xxxxxxxxxxxxx` |
| `nvd_api_key` | NVD API key for Dependency-Check | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |

### Optional Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `xcode_workspace_path` | `""` | Path to `.xcworkspace` (if using CocoaPods) |
| `podfile_path` | `""` | Path to `Podfile.lock` |
| `run_unit_test` | `off` | Run unit tests (`on`/`off`) |
| `test_plan_name` | `""` | Test plan name to execute |
| `run_dcheck` | `on` | Enable Dependency-Check (`on`/`off`) |
| `run_dtrack` | `off` | Enable Dependency-Track (`on`/`off`) |
| `run_periphery` | `on` | Enable Periphery (`on`/`off`) |
| `exclusion_file` | `**/*.xml,Pods/**/*,...` | File patterns to exclude |
| `extra_sonar_param` | `""` | Additional parameters for sonar-scanner |
| `verbose_mode_enabled` | `off` | Verbose mode (`on`/`off`) |

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the project
2. Create a branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 💬 Support

If you encounter issues or have questions:

- Open an [issue on GitHub](https://github.com/neopixl/bitrise-step-sonarqube-ios/issues)

---

**Built with ❤️ by [Neopixl](https://github.com/neopixl)**
