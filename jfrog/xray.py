""" functions to manage Artifactory """

import logging
import requests
from tabulate import tabulate
from jfrog import utilities

HEADERS = {'content-type': 'application/json'}

# The different levels of logging, from highest urgency to lowest urgency, are:
# CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


def xray_ping(url, token):
    """
    This function is intented to get the health info of JFrog xray

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
    url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
        url)
    urltopost = url + "/xray/api/v1/system/ping"
    response = requests.get(urltopost, headers=HEADERS, timeout=30)
    if response.ok:
        logging.info("Your Xray Instance is currently healthy")
    else:
        logging.warning("Your Xray Instance may not be healthy")
        try:
            print(tabulate(response.json()))
        except ValueError:
            logging.warning("Please Xray is installed")
    return response


def xray_version(url, token):
    """
    This function is intented to get the version info of xray

    Parameters
    ----------
    arg1 : str
        base URL of JFrog Platform
    arg2 : str
        access or identity token of admin account

    Returns
    -------
    str
        version of xray
    """
    HEADERS.update({"Authorization": "Bearer " + token})
    url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
        url)
    urltopost = url + "/xray/api/v1/system/version"
    response = requests.get(urltopost, headers=HEADERS, timeout=30)
    if response.ok:
        versioninfo = response.json()
        logging.info(
            "Your Xray Instance is currently running %s", versioninfo['xray_version'])
        version = versioninfo['xray_version']
    else:
        logging.error("Could not determin the Xray version")
        print(tabulate(response.json()))
        version = 0.0
    return version
