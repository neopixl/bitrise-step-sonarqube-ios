# Sonarqube

This step run some utilities to check the quality of your code, scans the results, and upload them to your Sonarqube server.


## How to use this Step

### Add the Step to a Workflow
Reference it in your `bitrise.yml` with the `git::PUBLIC-GIT-CLONE-URL@BRANCH` step reference style:

```
- git::https://github.com/neopixl/bitrise-step-sonarqube-ios:
   inputs:
   - project_key: client-project
   - exclusions: "**/*.xml,Pods/**/*,Reports/**/*"
```

The `project_key` and `exclusions` are editable as well with the Bitrise UI, as well as other options (Swiftlint, tests, etc.)

### Add secret value

In order to upload results to you Sonar server, a secret environment variable is required:

1. `$SONAR_HOST_LOGIN`, containing the authorization token for your server.

## How to contribute to this Step

1. Fork this repository
2. `git clone` it
3. Create a branch you'll work on
4. To use/test the step just follow the **How to use this Step** section
5. Do the changes you want to
6. Run/test the step before sending your contribution
  * You can also test the step in your `bitrise` project, either on your Mac or on [bitrise.io](https://www.bitrise.io)
  * You just have to replace the step ID in your project's `bitrise.yml` with either a relative path, or with a git URL format
  * (relative) path format: instead of `- original-step-id:` use `- path::./relative/path/of/script/on/your/Mac:`
  * direct git URL format: instead of `- original-step-id:` use `- git::https://github.com/user/step.git@branch:`
  * You can find more example of alternative step referencing at: https://github.com/bitrise-io/bitrise/blob/master/_examples/tutorials/steps-and-workflows/bitrise.yml
7. Once you're done just commit your changes & create a Pull Request