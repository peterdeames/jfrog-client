""" functions to manage Artifactory """

import logging
import requests

HEADERS = {'content-type': 'application/json'}
JAVATYPES = ['maven', 'gradle', 'ivy']

# The different levels of logging, from highest urgency to lowest urgency, are:
# CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG
)


def get_repo_count(url, token, repository_type):
    """
    This function returns the count of the repository type passed to repository_type
    Valid options are: local|remote|virtual|federated|distribution
    """
    HEADERS.update({"Authorization": "Bearer " + token})
    urltopost = url + f'/ api/repositories?type = {repository_type}'
    response = requests.get(urltopost, headers=HEADERS, timeout=30)
    repos = response.json()
    return len(repos)
