import os
import sys
import logging
from jira import JIRA

class Vulnerability:
    
    #This class receives the organization -> repository -> vulnerabilityAlerts -> edges -> node data from Github GraphQL API
    #The data argument containt the vulnerability attributes to create the object
    
    def __init__(self,data):
        
        self._id = data['node']['id']
        self._createdAt = data['node']['createdAt']
        self._fixedAt = data['node']['fixedAt']
        self._state = data['node']['state']
        self._repositoryname = data['node']['repository']['name']
        self._repositoryurl = data['node']['repository']['url']
        self._description = data['node']['securityAdvisory']['description']
        self._severity = data['node']['securityAdvisory']['severity']
        self._title = data['node']['securityAdvisory']['summary']
        
                
    def map_jira_issues(self):
        
        #Get authentication strings from enviroment variable
        
        #Validate if those variables are set
        env_vars = ["JIRA_URL", "JIRA_TOKEN", "JIRA_EMAIL", "JIRA_PROJECT_ID", "UID_CUSTOMFIELD_ID", "JIRA_COMPLETE_PHASE_ID", "JIRA_START_PHASE_ID"]
        missing_vars = []
        for var in env_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if len(missing_vars) == 0:                
            jira_url = os.getenv("JIRA_URL")
            jira_token = os.getenv("JIRA_TOKEN")
            jira_email = os.getenv("JIRA_EMAIL")
            project_id = os.getenv("JIRA_PROJECT_ID")
            uid_customfield_id = os.getenv("UID_CUSTOMFIELD_ID")
            complete_phase_id = os.getenv("JIRA_COMPLETE_PHASE_ID")
            start_phase_id = os.getenv("JIRA_START_PHASE_ID")
            
        else:
            
            logging.error(f"You need to setup the variables {' ,'.join(missing_vars)}")
            sys.exit(1)
        
        #Create jira connection
        
        jira = JIRA(jira_url, basic_auth=(jira_email,jira_token))
            
        
        #Mapping Issues
        #The document says that the search.issues returns only 50 issues, check the 'maxResults' or pagination possibilities
        
        vulnerabilities_in_board = jira.search_issues(f'project={project_id} AND labels = github_vulnerability', maxResults=1000)
        
        #Check if vulnerability object is mapped in Jira's board, if not, create it
            
        if self.check_if_vulnerability_is_mapped(vulnerabilities_in_board, uid_customfield_id):
                
            #Update existing vulnerability information
            self.update_vulnerability(jira, vulnerabilities_in_board, uid_customfield_id, complete_phase_id, start_phase_id)
           
        else:
                
            self.create_vulnerability(jira, project_id, uid_customfield_id, complete_phase_id)

            
    def create_vulnerability(self, jira, project_id, uid_customfield_id, complete_phase_id):
        
        issue_type = os.getenv('JIRA_ISSUE_TYPE', 'Task')
        labels = [f"{self._repositoryname}", f"{self._state}", "github_vulnerability", f"{self._severity}"]
        
        vulnerability_attributes = {
            
            f'{uid_customfield_id}': f'{self._id}',
            'project': f'{project_id}',
            'summary': f'{self._title}',
            'description': f'{self._description} *Repository:* [{self._repositoryurl}]',
            'issuetype': {'name': f'{issue_type}'},
            'labels': labels
            
            
        }
        
        new_issue = jira.create_issue(fields=vulnerability_attributes)
        
        
        #If the state of the vulnerability is not open, update the recently created Jira's issue status
        if self._state != "OPEN":
            
            jira.transition_issue(new_issue.key, complete_phase_id)
            
    
    def update_vulnerability(self, jira, vulnerabilities_in_board, uid_customfield_id, complete_phase_id, start_phase_id):
        
        for issue in vulnerabilities_in_board:
            
            #The "state id of the status" is different than "transition id of status", this will get the state id of status of the current transition
               
            for id in jira.transitions(issue):
                
                if id['id'] == complete_phase_id:
                    
                    complete_state_id = id['to']['statusCategory']['id']
                
                if id['id'] == start_phase_id:
                    
                    start_state_id = id['to']['statusCategory']['id']
                
                    
            #If the state of the vulnerability object is different than "OPEN", moves it to complete phase
                    
            if self._id == getattr(issue.fields, uid_customfield_id) and self._state != "OPEN" and issue.fields.status.id == complete_state_id:
                
                jira.transition_issue(issue.key, complete_phase_id)
            
            #If the state of the vulnerability object is equal to "OPEN", moves it to start phase. This will guarantee that if a vulnerability get the state "OPEN" again, it will moves it to start phase
                            
            if self._id == getattr(issue.fields, uid_customfield_id) and self._state == "OPEN" and issue.fields.status.id != start_state_id:
                
                jira.transition_issue(issue.key, start_phase_id)
                
                
    def check_if_vulnerability_is_mapped(self, vulnerabilities_in_board, uid_customfield_id):
        
        vulnerability_exist = False
        
        #Check if vulnerability exist in Jira's project, if don't, call create_vulnerability() method
        
        for issue in vulnerabilities_in_board:
            
            #Check if the vulnerability ID is equal to Jira's issue UID field "customfield_{number}"
                
            if self._id == getattr(issue.fields, uid_customfield_id):
                    
                vulnerability_exist = True
                return vulnerability_exist
                
        return vulnerability_exist
