""" functions to support the JFrog Platform """

import logging
import requests
from tabulate import tabulate

HEADERS = {'content-type': 'application/json'}

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
    urltopost = url + "/api/system/ping"
    response = requests.get(urltopost, headers=HEADERS, timeout=30)
    if response.ok:
        logging.info("Your Artifactory Instance is currently healthy")
    else:
        logging.error("Your Artifactory Instance is not healthy")
        logging.error(response.text)
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
    urltopost = url + "/api/system/version"
    response = requests.get(urltopost, headers=HEADERS, timeout=30)
    versioninfo = response.json()
    if response.ok:
        logging.info(
            "Your Artifactory Instance is currently running %s", versioninfo['version'])
    else:
        logging.error("Could not determin the Artifactory version")
        logging.error(response.text)
    return versioninfo['version']


def xray_ping(url, token):
    """
    This function is intented to get the health info of Jfrog xray

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
    urltopost = url + "/api/v1/system/ping"
    response = requests.get(urltopost, headers=HEADERS, timeout=30)
    if response.ok:
        logging.info("Your Xray Instance is currently healthy")
    else:
        logging.error("Your Xray Instance is not healthy")
        logging.error(response.text)
    return response


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
    urltopost = url + "/api/system/license"
    response = requests.get(urltopost, headers=HEADERS, timeout=30)
    result = response.json()
    print(tabulate(result.items()))
    return result
