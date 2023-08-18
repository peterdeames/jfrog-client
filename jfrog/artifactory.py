""" functions to manage Artifactory """

import logging
import requests
from tabulate import tabulate
from jfrog import utilities

HEADERS = {'content-type': 'application/json'}
JAVATYPES = ['maven', 'gradle', 'ivy']

# The different levels of logging, from highest urgency to lowest urgency, are:
# CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


def artifactory_ping(url, token):
    """
    This function is intented to get the health info of Jfrog Platform

    Parameters
    ----------
    arg1 : str
        base URL of JFrog Platform
    arg2 : str
        access or identity token of admin account

    Returns
    -------
    str
        reponse
    """
    HEADERS.update({"Authorization": "Bearer " + token})
    url = utilities.__validate_url(url)  # pylint: disable=W0212
    urltopost = url + "/artifactory/api/system/ping"
    try:
        response = requests.get(urltopost, headers=HEADERS, timeout=30)
        if response.ok:
            logging.info("Your Artifactory Instance is currently healthy")
        else:
            logging.warning("Your Artifactory Instance may not be healthy")
            print(tabulate(response.json()))
    except requests.ConnectionError as err:
        print("Some other error happened:", err)

    return response


def artifactory_version(url, token):
    """
    This function is intented to get the version info of Jfrog Platform

    Parameters
    ----------
    arg1 : str
        base URL of Jfrog PLatform
    arg2 : str
        access or identity token of admin account

    Returns
    -------
    str
        version of artifactory
    """
    HEADERS.update({"Authorization": "Bearer " + token})
    url = utilities.__validate_url(url)  # pylint: disable=W0212
    urltopost = url + "/artifactory/api/system/version"
    response = requests.get(urltopost, headers=HEADERS, timeout=30)
    if response.ok:
        versioninfo = response.json()
        logging.info(
            "Your Artifactory Instance is currently running %s", versioninfo['version'])
        version = versioninfo['version']
    else:
        logging.error("Could not determin the Artifactory version")
        print(tabulate(response.json()))
        version = 0.0
    return version


def get_license_details(url, token):
    """
    This function is intented to get the license info of Jfrog Platform

    Parameters
    ----------
    arg1 : str
        base URL of Jfrog Platform
    arg2 : str
        access or identity token of admin account

    Returns
    -------
    dict
        dictionary of license information
    """
    HEADERS.update({"Authorization": "Bearer " + token})
    url = utilities.__validate_url(url)  # pylint: disable=W0212
    urltopost = url + "/artifactory/api/system/license"
    response = requests.get(urltopost, headers=HEADERS, timeout=30)
    if response.ok:
        result = response.json()
    else:
        logging.error("Unable to get license information")
        print(tabulate(response.json()))
        result = {"type": "-", "validThrough": "-", "licensedTo": "-"}
    return result


def get_ha_nodes(url, token):
    """
    This function is intented to get the count of nodes in a Jfrog Platform HA setup

    Parameters
    ----------
    arg1 : str
        base URL of Jfrog Platform
    arg2 : str
        access or identity token of admin account

    Returns
    -------
    int
        number of nodes
    """
    HEADERS.update({"Authorization": "Bearer " + token})
    url = utilities.__validate_url(url)  # pylint: disable=W0212
    urltopost = url + "/artifactory/api/system/licenses"
    response = requests.get(urltopost, headers=HEADERS, timeout=30)
    if response.ok:
        result = response.json()
        nodes = len(result['licenses'])
    else:
        logging.error("Unable to get node information")
        print(tabulate(response.json()))
        nodes = 0
    return nodes


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
    url = utilities.__validate_url(url)  # pylint: disable=W0212
    urltopost = url + f'/artifactory/api/repositories?type = {repository_type}'
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


def get_storage_info(url, token):
    """
    This function returns the storage information

    Parameters
    ----------
    arg1 : str
        base URL of Jfrog PLatform
    arg2 : str
        access or identity token of admin account

    Returns
    -------
    dict
        dictionary of storage information
    """
    HEADERS.update({"Authorization": "Bearer " + token})
    url = utilities.__validate_url(url)  # pylint: disable=W0212
    urltopost = url + '/artifactory/api/storageinfo'
    response = requests.get(urltopost, headers=HEADERS, timeout=30)
    if response.ok:
        storageinfo = response.json()
        storageinfo = storageinfo['binariesSummary']
    else:
        logging.error("Unable to get storage information")
        storageinfo = {'binariesCount': '0', 'binariesSize': '0 GB', 'artifactsSize': '0 GB',
                       'optimization': '0%', 'itemsCount': '0', 'artifactsCount': '0'}
    return storageinfo


def setdata(name, layout, ptype, rtype):
    """ This function sets the data to be sent for the creation of a repo """
    return '{"key":"' + name + '","rclass":"' + rtype + '","packageType":"' + ptype + '", "xrayIndex":true,"repoLayoutRef":"' + layout + '"}'


def rename_repo(url, token, old_repo_name, new_repo_name, ptype, action='copy', delete=False):
    """
    This function will rename a repository by creating a new repo and moving the contents
    New repo will be created with default values

    Parameters
    ----------
    arg1 : str
        base URL of JFrog Platform
    arg2 : str
        access or identity token of admin account
    arg3 : str
        old repo name
    arg4 : str
        new repo name
    arg5 : str
        package type for the new repo
    arg6 : str
        action to be taken with the contents
        valid options are copy or move
    arg7 : bool
        True or False flag to delete the old repo when action is complete

    """
    HEADERS.update({"Authorization": "Bearer " + token})
    url = utilities.__validate_url(url)  # pylint: disable=W0212
    # get type of old repo
    # TODO: get the type of repo to setup
    rtype = 'local'
    # create new repo
    urltopost = url + f'/artifactory/api/repositories/{new_repo_name}'
    layout = utilities.__setlayout(ptype)  # pylint: disable=W0212
    data = setdata(new_repo_name, layout, ptype, rtype)
    response = requests.put(urltopost, headers=HEADERS, data=data, timeout=30)
    if response.ok:
        logging.info(response.reason)
        # copy/move contents
        urltopost = url + \
            f'/artifactory/api/storage/{old_repo_name}?list&deep=1'
        response = requests.get(urltopost, headers=HEADERS, timeout=30)
        json_object = response.json()
        items = json_object["files"]
        for item in items:
            uri = item.get('uri')
            urltopost = url + \
                f'/artifactory/api/copy/{old_repo_name}{uri}?to=/{new_repo_name}{uri}'
            response = requests.post(urltopost, headers=HEADERS, timeout=30)
            logging.info(utilities.__get_msg(response, 'messages'))
        # TODO: delete old repo
    else:
        logging.error(utilities.__get_msg(response, 'errors'))
