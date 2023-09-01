""" functions to manage Artifactory """

import json
import logging
from datetime import datetime

import requests
from tqdm import tqdm
from tabulate import tabulate

from jfrog import artifactory, utilities

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
    count = 0
    current_version = artifactory.artifactory_version(url, token)
    if utilities.__checkversion(current_version, "7.49.3"):  # pylint: disable=W0212:protected-access
        HEADERS.update({"Authorization": "Bearer " + token})
        url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
            url)
        urltopost = url + "/access/api/v2/users"
        response = requests.get(urltopost, headers=HEADERS, timeout=30)
        userinfo = response.json()
        userinfo = userinfo['users']
        if user_type is None:
            count = len(userinfo)
        else:
            for user in userinfo:
                if user['realm'] == user_type:
                    count += 1
    else:
        logging.error(
            "Can't get the count of users as the version of artifactory is < 7.49.3")
    return count


def get_tokens(url, token, export=False):
    """
    Returns token information, based on the authenticated principal

    An admin user can get all tokens and \n
    Non-admin users only gets the tokens where their username matches the tokens' username

    Parameters
    ----------
    arg1 : str
        base URL of JFrog Platform
    arg2 : str
        access or identity token of admin account
    arg3 : bool
        flag to determine if an output file should be created

    Returns
    -------
    list
        list of dictionaries of token information
    """
    current_version = artifactory.artifactory_version(url, token)
    if utilities.__checkversion(current_version, "7.21.1"):  # pylint: disable=W0212:protected-access
        t_headers = ['ID', 'Subject', 'Issued',
                     'Issuer', 'Expiry', 'Refreshable']
        HEADERS.update({"Authorization": "Bearer " + token})
        url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
            url)
        urltopost = url + "/access/api/v1/tokens"
        response = requests.get(urltopost, headers=HEADERS, timeout=30)
        tokens = response.json()
        tokens = tokens['tokens']
        table = []
        for t_id in tokens:
            token_lst = []
            token_lst.append(t_id['token_id'])
            token_lst.append(t_id['subject'])
            datetime_obj = datetime.utcfromtimestamp(t_id['issued_at'])
            token_lst.append(datetime_obj.strftime("%d-%m-%Y %H:%M:%S"))
            token_lst.append(t_id['issuer'])
            try:
                datetime_obj = datetime.utcfromtimestamp(t_id['expiry'])
                token_lst.append(datetime_obj.strftime("%d-%m-%Y %H:%M:%S"))
            except KeyError:
                token_lst.append('')
            token_lst.append(t_id['refreshable'])
            table.append(token_lst)
        if export and len(table) > 0:
            print()
            print(tabulate(table, headers=t_headers))
            print()
            with open('output.txt', 'w', encoding='utf-8') as file:
                file.write(tabulate(table, headers=t_headers))
    else:
        logging.error(
            "Can't create a token as the version of artifactory is < 7.21.1")
        tokens = {}
    return tokens


def create_token(url, token, description, scope=None, expires_in=None,  # pylint: disable=R0913
                 refreshable=False, username=None, project_key=None):
    """
    This function will create a new token

    Parameters
    ----------
    arg1 : str
        base URL of JFrog Platform
    arg2 : str
        access or identity token of admin account
    arg3 : str
        free text token description. Useful for filtering and managing tokens.
    arg4 : str
        The following scopes are supported.
        applied-permissions/user (default)
        applied-permissions/admin
        applied-permissions/groups format: applied-permissions/groups:<group-name>[,<group-name>...]
        system:metrics:r- for getting the service metrics
        system:livelogs:r - for getting the service livelogsr
    arg5 : int
        the amount of time, in seconds, it would take for the token to expire
        set to 0 to apply the syetem default
    arg6 : bool
        if the token should be refreshable
    arg7 : str
        username for which this token is to be created for
    arg8 : str
        project for which this token is to be created for

    Returns
    -------
    dict
        dictionary of token information
    """
    current_version = artifactory.artifactory_version(url, token)
    if utilities.__checkversion(current_version, "7.21.1"):  # pylint: disable=W0212:protected-access
        HEADERS.update({"Authorization": "Bearer " + token})
        url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
            url)
        urltopost = url + "/access/api/v1/tokens"
        data = utilities.__set_token_data(  # pylint: disable=W0212:protected-access disable=E1121:too-many-function-args
            description, scope, expires_in, refreshable, username, project_key)
        response = requests.post(
            urltopost, headers=HEADERS, data=data, timeout=30)
        token = response.text
    else:
        logging.error(
            "Can't create a token as the version of artifactory is < 7.21.1")
        token = ''
    return token


def get_default_token_expiry(url, token):
    """
    This function return the default token expiry in seconds

    Parameters
    ----------
    arg1 : str
        base URL of JFrog Platform
    arg2 : str
        access or identity token of admin account

    Returns
    -------
    dict
        dictionary of token information
    """
    HEADERS.update({"Authorization": "Bearer " + token})
    url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
        url)
    current_version = artifactory.artifactory_version(url, token)
    if utilities.__checkversion(current_version, "7.62.0"):  # pylint: disable=W0212:protected-access
        urltopost = url + "/access/api/v1/tokens/default_expiry"
        response = requests.get(urltopost, headers=HEADERS, timeout=30)
        if response.ok:
            expiryinfo = response.json()
            expiry = expiryinfo['default_expiry']
            logging.info(
                "The default for a token expiry is set to %s seconds", expiry)
    else:
        logging.error(
            "Can't get the default token expiry as the version of artifactory is < 7.62.x")
        expiry = 0.0
    return expiry


def set_default_token_expiry(url, token, expiry):
    """
    This function set a new default token expiry in seconds

    Parameters
    ----------
    arg1 : str
        base URL of JFrog Platform
    arg2 : str
        access or identity token of admin account
    arg3 : int
        default token expoiry in seconds
    """
    data = {}
    data["default_expiry"] = expiry
    HEADERS.update({"Authorization": "Bearer " + token})
    url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
        url)
    current_version = artifactory.artifactory_version(url, token)
    if utilities.__checkversion(current_version, "7.62.0"):  # pylint: disable=W0212:protected-access
        urltopost = url + "/access/api/v1/tokens/default_expiry"
        # TODO: Check what is returned and output a validation message
        requests.put(urltopost, headers=HEADERS, data=data, timeout=30)
    else:
        logging.error(
            "Can't set the default token expiry as the version of artifactory is < 7.62.x")


def create_support_bundle(url, token, name, description, dic_config=None):
    """
    This function creates a new Support bundle

    Parameters
    ----------
    arg1 : str
        base URL of JFrog Platform
    arg2 : str
        access or identity token of admin account
    arg3 : str
        name for the bundle to be created
    arg4 : str
        description for the bundle to be created
    arg5 : dict
        dictionary of optional configuration for the bundle\n
            {
                "parameters":{
                    "configuration": "",
                    "system": "",
                    "logs":{"include": "", "start_date":"YYYY-MM-DD","end_date":"YYYY-MM-DD"}
                },
                "thread_dump":{
                    "count": 1,
                    "interval": 0
                }
            }

    Returns
    -------
    str
        id of the created bundle
    """
    if dic_config is None:
        dic_config = {}
    data = {**dic_config}
    data["name"] = name
    data["description"] = description
    data = json.dumps(data)
    HEADERS.update({"Authorization": "Bearer " + token})
    url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
        url)
    urltopost = url + "/artifactory/api/system/support/bundle"
    logging.info('Generating a New Support Bundle')
    response = requests.post(urltopost, headers=HEADERS, data=data, timeout=30)
    if response.ok:
        logging.info(response.text)
        bundleinfo = response.json()
        bundle_id = bundleinfo['id']
    else:
        logging.error(utilities.__get_msg(response, 'errors')  # pylint: disable=W0212:protected-access
                      )
        bundle_id = ''
    return bundle_id


def get_support_bundle(url, token, bundle_id):
    """
    This function downloads a support bundle

    Parameters
    ----------
    arg1 : str
        base URL of JFrog Platform
    arg2 : str
        access or identity token of admin account
    arg3 : str
        id of the bundle to be downloaded

    """
    HEADERS.update({"Authorization": "Bearer " + token})
    url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
        url)
    urltopost = url + \
        f"/artifactory/api/system/support/bundle/{bundle_id}/archive"
    with open(f'{bundle_id}.zip', 'wb') as f:
        with requests.get(urltopost, headers=HEADERS, stream=True, timeout=300) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            tqdm_params = {
                'desc': 'Downloading Support Bundle',
                'total': total, 'miniters': 1, 'unit': 'B',
                'unit_scale': True, 'unit_divisor': 1024,
            }
            with tqdm(**tqdm_params) as pb:
                for chunk in r.iter_content(chunk_size=8192):
                    pb.update(len(chunk))
                    f.write(chunk)
