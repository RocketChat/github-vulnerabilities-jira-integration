import os
import json
import sys
import requests
import logging


def github_api_request(query):
    
    github_token = os.getenv('GITHUB_TOKEN')
    auth_header = {"Authorization": f"bearer {github_token}"}
    graphql_github_url = os.getenv("GITHUB_GRAPHQL_URL")
    
    if github_token is None:
        
        logging.error("You must declare the GITHUB_TOKEN enviroment variable")
        sys.exit(1)
    
    try:
        
        github_request = requests.post(graphql_github_url, json={'query': query}, headers=auth_header)
        github_request.raise_for_status()
        return json.loads(github_request.text)
    
    except requests.exceptions.RequestException as e:
        
        logging.error("Error occurred during GitHub API request: %s", str(e))
        sys.exit(1)
        
    except json.JSONDecodeError as e:
        
        logging.error("Error decoding JSON response from GitHub API: %s", str(e))
        sys.exit(1)


def generate_query(hasnextpage,nextpage=None):
    
        #Get variables from the Github action's environment
        name_of_organization = os.getenv("GITHUB_REPOSITORY_OWNER")
        name_of_repository = os.getenv("GITHUB_REPOSITORY").split("/")[-1]
        vulnerabilities_in_page = 100
        
        if hasnextpage:
            
            nextpage = f'"{nextpage}"'
            
        else:
            
            nextpage = "null"
            
        #Github GRAPHQL API query to get list of vulnerabilities from repository
        query = f"""
        {{
        organization(login: "{name_of_organization}") {{
            repository(name: "{name_of_repository}") {{
            vulnerabilityAlerts(first: {vulnerabilities_in_page}, after: {nextpage}) {{
                edges {{
                node {{
                    id
                    createdAt
                    fixedAt
                    state
                    securityAdvisory {{
                    severity
                    summary
                    description
                    }}
                    repository {{
                    name
                    url
                    }}
                    number
                }}
                }}
                pageInfo {{
                hasNextPage
                endCursor
                startCursor
                }}
            }}
            }}
        }}
        }}
        """
        
        return query
    
    
def create_vulnerability_list():

    hasnextpage=False
    query = generate_query(hasnextpage)
    github_response = github_api_request(query)
    
    hasnextpage = github_response['data']['organization']['repository']['vulnerabilityAlerts']['pageInfo']['hasNextPage']
    vulnerabilities = github_response['data']['organization']['repository']['vulnerabilityAlerts']['edges']
    
    if len(vulnerabilities) == 0:
        
        logging.warning("There's no vulnerability in this repository")
        sys.exit(1)
    
    #GrapQL API pagination
    while hasnextpage:
        
        #Get nextpage base64 identification
        nextpage = github_response['data']['organization']['repository']['vulnerabilityAlerts']['pageInfo']['endCursor']
        
        query = generate_query(hasnextpage,nextpage)
        github_response = github_api_request(query)
        
        #Get next page vulnerabilities
        vulnerabilities_page = github_response['data']['organization']['repository']['vulnerabilityAlerts']['edges']
        
        for vulnerability in vulnerabilities_page:
            
            vulnerabilities.append(vulnerability)
        
        #Check if have next page
        hasnextpage = github_response['data']['organization']['repository']['vulnerabilityAlerts']['pageInfo']['hasNextPage']
        
    return vulnerabilities