""" functions to manage Artifactory """

import logging
from jfrog import utilities

HEADERS = {'content-type': 'application/json'}
JAVATYPES = ['maven', 'gradle', 'ivy']

# The different levels of logging, from highest urgency to lowest urgency, are:
# CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG
)


def setname(team, ptype, maturity):
    """ This functions sets the name of the repo """
    repo_names = []
    if ptype.lower() in JAVATYPES:
        if ptype.lower() == 'maven':
            name = 'libs'
        else:
            name = ptype.lower()
        repo_names.append(team.lower() + '-' + name + '-release-local')
        repo_names.append(team.lower() + '-' + name + '-snapshot-local')
        repo_names.append(team.lower() + '-' + name + '-plugins-release-local')
        repo_names.append(team.lower() + '-' + name + '-plugins-snapshot-local')
    else:
        if maturity is None:
            repo_names.append(team.lower() + '-' + ptype.lower() + '-local')
        else:
            for mat in maturity:
                repo_names.append(team.lower() + '-' + ptype.lower() + '-' + mat.lower() + '-local')
    return repo_names


def setup_local_repo(url, team, ptype, maturity = None):
    """
    Function to setup a local repository.

    This function is intented setup a local repository within Artifactory

    Parameters
    ----------
    arg1 : str
        base URL of Artifactory
    arg2 : str
        token of account to setup the project
    arg3 : str
        team or product name as the primary identifier of the project
    arg4 : str
        type of tool or package of the repo to be created
    arg5 : list (optional)
        list of package maturity levels, such as the development, staging and release

    """
    name = setname(team, ptype, maturity)
    logging.debug(name)
    layout = utilities.setlayout(ptype)
    logging.debug(layout)
