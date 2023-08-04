""" functions to manage Artifactory """

import logging
import requests
from tabulate import tabulate

HEADERS = {'content-type': 'application/json'}
JAVATYPES = ['maven', 'gradle', 'ivy']

# The different levels of logging, from highest urgency to lowest urgency, are:
# CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG
)


def get_repo_count(url, token, repository_type):
    """
    This function returns the count of the repository type passed to

    Parameters
    ----------
    arg1 : str
        base URL of Jfrog PLatform
    arg2 : str
        access or identity token of admin account
    arg3 : str
        repository_type
        Valid options are: local|remote|virtual|federated|distribution

    Returns
    -------
    int
        number of repositories
    """
    HEADERS.update({"Authorization": "Bearer " + token})
    urltopost = url + f'/api/repositories?type = {repository_type}'
    response = requests.get(urltopost, headers=HEADERS, timeout=30)
    if response.ok:
        repos = response.json()
        count = len(repos)
    else:
        logging.error("Unable to get count of %s repositories",
                      repository_type)
        print(tabulate(response.json()))
        count = 0
    return count
