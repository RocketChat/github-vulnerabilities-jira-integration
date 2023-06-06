# Github Vulnerabilities - Jira Project Integration


This tool enables the integration of GitHub vulnerabilities with a Jira project, automating the process of managing vulnerabilities between these platforms. It is designed to be used as a GitHub action, providing seamless integration into your development workflow. The tool performs the following actions:

**Closing Vulnerability Issues**: The tool checks the status of vulnerabilities in GitHub and automatically closes the corresponding issue in the Jira project.

**Updating Vulnerability Status**: It monitors changes in vulnerability status in GitHub. If a vulnerability changes from "open" to another state, the tool opens the corresponding issue in Jira, ensuring that your vulnerability management is synchronized across platforms.

## Configuration Steps

**JIRA**:

1. Set up a custom field in your Jira project that will be used by this tool to identify vulnerabilities.
2. Obtain the custom field ID by following the instructions in this link https://confluence.atlassian.com/jirakb/how-to-find-any-custom-field-s-ids-744522503.html. Insert the custom field ID in the GitHub action variable (refer to the Variables section).
3. Obtain the transaction ID for the "Completed" or "Backlog" status. This ID will be used to automatically close vulnerabilities in your Jira project when they are closed in GitHub. For guidance on finding the transaction ID, refer to this community post https://community.atlassian.com/t5/Jira-questions/How-to-fine-transition-ID-of-JIRA/qaq-p/1207483.

**Github**:

1.  It is important to create a secret in your repository with permission to access vulnerability information. In our tests, we observed that the default GitHub actions variable "GITHUB_TOKEN" does not work for this purpose. Refer to the Variables section for details.

## Variables

To use this tool as a GitHub action, you need to set the following variables in your GitHub action configuration:

**GITHUB_TOKEN:** A GitHub token that integrates with your repository. We recommend adding a "_GITHUB_TOKEN" secret with "_" to your action secrets instead of using the default "GITHUB_TOKEN" since thIS variable is a reserved variable and cannot be used.

**JIRA_URL:** The URL of your Jira instance.

**JIRA_TOKEN:** A token or API key with sufficient permissions to access Jira.

**JIRA_EMAIL:** The email associated with your Jira account.

**JIRA_PROJECT_ID:** The ID of the Jira project where the vulnerability issues will be created. For example, if the Jira project URL is https://example.atlassian.net/jira/software/c/projects/TST/boards/63, the project will be **TST**.

**UID_CUSTOMFIELD_ID:** The ID of the custom field in Jira to store the vulnerability UID.

**JIRA_COMPLETE_PHASE_ID:** The ID of the transaction where the issue goes to the complete phase.

**JIRA_START_PHASE_ID:** The ID of the transaction where the issue goes to the backlog phase. 


## Integration with GitHub Action

Here is an example of how to integrate this GitHub action:

```
name: Github vulnerabilities and jira project integration

on:
  schedule:
    - cron: '0 */6 * * *'
      
jobs:
  IntegrateSecurityVulnerabilities:
    runs-on: ubuntu-latest
    steps:
      - name: "Github vulnerabilities and jira project integration"
        uses: RocketChat/github-vulnerabilities-jira-integration@v0.1
        env:
          JIRA_URL: https://example.atlassian.net/
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
