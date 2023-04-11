""" functions to support the JFrog Platform """

import logging
import requests
from tabulate import tabulate

HEADERS = {'content-type': 'application/json'}

# The different levels of logging, from highest urgency to lowest urgency, are:
# CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG
)


def artifactory_ping(url, token):
    """
    Function to return the health of Artifactory
    """
    HEADERS.update({"Authorization": "Bearer " + token})
    urltopost = url + "/api/system/ping"
    response = requests.get(urltopost, headers=HEADERS, timeout=30)
    if response.ok:
        logging.info("Your Artifactory Instance is currently healthy")
    else:
        logging.error("Your Artifactory Instance is not healthy")
        logging.error(response.text)
    return response.text


def xray_ping(url, token):
    """
    Function to return the health of Xray
    """
    HEADERS.update({"Authorization": "Bearer " + token})
    urltopost = url + "/api/v1/system/ping"
    response = requests.get(urltopost, headers=HEADERS, timeout=30)
    if response.ok:
        logging.info("Your Xray Instance is currently healthy")
    else:
        logging.error("Your Xray Instance is not healthy")
        logging.error(response.text)
    return response.text


def get_license_details(url, token):
    """
    Function to get system license info

    This function is intented to get the license info of Jfrog Platform

    Parameters
    ----------
    arg1 : str
        base URL of Jfrog PLatform
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
