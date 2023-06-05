from github_helper import create_vulnerability_list
import jira_processor
import sys


def main():
    vulnerabilities = create_vulnerability_list()

    for data in vulnerabilities:
    
        vulnerability = jira_processor.Vulnerability(data)
        jira_issue = vulnerability.map_jira_issues()
  
if __name__ == '__main__':
    main()
