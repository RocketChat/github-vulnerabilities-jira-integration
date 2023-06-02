# github-security-alerts-jira-integration
A tool to get vulnerabilities alerts from Github's security report and create issues in Jira

Overall comments:

1. Here is some parameters that needs to insert in the github actions: JIRA_URL, JIRA_TOKEN, JIRA_EMAIL, JIRA_PROJECT_ID, GITHUB_TOKEN, UID_CUSTOMFIELD_ID, JIRA_ISSUE_TYPE, JIRA_COMPLETE_PHASE_ID and JIRA_START_PHASE_ID (https://community.atlassian.com/t5/Jira-questions/How-to-fine-transition-ID-of-JIRA/qaq-p/1207483)
2. Here is the expected default parameters of github actions: GITHUB_GRAPHQL_URL, GITHUB_REPOSITORY_OWNER, GITHUB_REPOSITORY https://docs.github.com/en/actions/learn-github-actions/variables