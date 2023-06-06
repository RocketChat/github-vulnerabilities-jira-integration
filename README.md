# Github Vulnerabilities - Jira Board Integration


This tool enables the integration of GitHub vulnerabilities with a Jira board, automating the process of managing vulnerabilities between these platforms. It is designed to be used as a GitHub action, providing seamless integration into your development workflow. The tool performs the following actions:

**Closing Vulnerability Issues**: The tool checks the status of vulnerabilities in GitHub and automatically closes the corresponding issue in the Jira board.

**Updating Vulnerability Status**: It monitors changes in vulnerability status in GitHub. If a vulnerability changes from "open" to another state, the tool opens the corresponding issue in Jira, ensuring that your vulnerability management is synchronized across platforms.

To use this tool as a GitHub action, you need to set the following variables in your GitHub action configuration:

**JIRA_URL:** The URL of your Jira instance.

**JIRA_TOKEN:** A token or API key with sufficient permissions to access Jira.

**JIRA_EMAIL:** The email associated with your Jira account.

**JIRA_PROJECT_ID:** The ID of the Jira project where the vulnerability issues will be created. (Eg: https://rocketchat.atlassian.net/jira/software/c/projects/SB/boards/63 will be: **SB**)

**UID_CUSTOMFIELD_ID:** The ID of the custom field in Jira to store the vulnerability UID. (https://confluence.atlassian.com/jirakb/how-to-find-any-custom-field-s-ids-744522503.html)

**JIRA_COMPLETE_PHASE_ID:** The ID of the transaction where the issue goes to the complete phase. (https://community.atlassian.com/t5/Jira-questions/How-to-fine-transition-ID-of-JIRA/qaq-p/1207483)

**JIRA_START_PHASE_ID:** The ID of the transaction where the issue goes to the backlog phase. (https://community.atlassian.com/t5/Jira-questions/How-to-fine-transition-ID-of-JIRA/qaq-p/1207483)

**GITHUB_TOKEN:** The GitHub token with the necessary permissions to access the repository and create/update issues.

## Integrate this Github Action

Here is an example in how to integrate this github action:

```
name: Github vulnerabilities and jira board integration

on:
  push:
    branches:
      - main
      
jobs:
  IntegrateSecurityVulnerabilities:
    runs-on: ubuntu-latest
    steps:
      - name: "Github vulnerabilities and jira board integration"
        uses: RocketChat/github-vulnerabilities-jira-integration@v0.1
        env:
          JIRA_URL: https://rocketchat.atlassian.net/
          JIRA_TOKEN: ${{ secrets.JIRA_TOKEN }}
          GITHUB_TOKEN: ${{ secrets._GITHUB_TOKEN }}
          JIRA_EMAIL: security@rocket.chat
          JIRA_PROJECT_ID: GJIT
          UID_CUSTOMFIELD_ID: customfield_10059
          JIRA_COMPLETE_PHASE_ID: 31
          JIRA_START_PHASE_ID: 11
```

Please ensure that you have properly configured these variables in your GitHub action environment for the tool to function correctly.

Note: This tool assumes that you have already set up Jira and GitHub repositories for vulnerability management and have the necessary permissions to perform the required actions.

For any issues, suggestions, or contributions, please refer to the project repository and its maintainers.
