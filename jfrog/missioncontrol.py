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


def missioncontrol_ping(url, token):
    """
    This function is intented to get the health info of JFrog Platform

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
    urltopost = url + "/mc/api/system/ping"
    response = requests.get(urltopost, headers=HEADERS, timeout=30)
    if response.ok:
        logging.info("Your Mission Control Instance is currently healthy")
    else:
        logging.warning("Your Mission Control Instance may not be healthy")
        try:
            print(tabulate(response.json()))
        except ValueError:
            logging.warning("Please Mission Control is installed")
    return response
