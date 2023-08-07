""" functions to manage Artifactory """

import logging
import requests
from jfrog import utilities

HEADERS = {'content-type': 'application/json'}

# The different levels of logging, from highest urgency to lowest urgency, are:
# CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


def get_users(url, token, user_type=None):
    """
    This function returns the count of the user type passed to user_type
    If user_type is not passed it will return total user count

    Parameters
    ----------
    arg1 : str
        base URL of JFrog Platform
    arg2 : str
        access or identity token of admin account
    arg3: string
        type of user to be counted
        Valid options are: internal|saml|scim

    Returns
    -------
    int
        number of users
    """
    HEADERS.update({"Authorization": "Bearer " + token})
    url = utilities.__validate_url(url)  # pylint: disable=W0212
    urltopost = url + "/access/api/v2/users"
    response = requests.get(urltopost, headers=HEADERS, timeout=30)
    userinfo = response.json()
    userinfo = userinfo['users']
    count = 0
    if user_type is None:
        count = len(userinfo)
    else:
        for user in userinfo:
            if user['realm'] == user_type:
                count += 1
    return count
