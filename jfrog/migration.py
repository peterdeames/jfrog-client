""" functions to enable the migration of JFrog Platform """

import json
import logging
from ast import literal_eval
import requests
from jfrog import utilities

HEADERS = {'content-type': 'application/json'}

# The different levels of logging, from highest urgency to lowest urgency, are:
# CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


def __check_offline(source_config):
    """ check if the remote repo is marked offline so it will not migrate """
    logging.debug(source_config.text)
    json_object = json.loads(source_config.text)
    logging.debug(json_object)
    logging.debug(json_object["offline"])
    return json_object["offline"]


def __setdata(url, repo, user, pwd):
    """ this function sets the data to be posted to Artifactory """
    data = {}
    data["url"] = url
    data["repoKey"] = repo
    data["username"] = user
    data["password"] = pwd
    data["enableEventReplication"] = 'true'
    data["enabled"] = 'true'
    data["cronExp"] = "0 0 4 ? * *"
    data["syncDeletes"] = 'true'
    data["syncProperties"] = 'true'
    data["syncStatistics"] = 'true'
    data = json.dumps(data)
    return data


def sync_local_repos(source_url, source_token, target_url, target_token, user):
    """
    This function is intented to compare the local repos and setup anything missing on the target JFP

    Parameters
    ----------
    arg1 : str
        base URL of the source JFrog Platform
    arg2 : str
        identity token of admin account for the source JFrog Platform
    arg3 : str
        base URL of the target JFrog Platform
    arg4 : str
        identity token of admin account for the target JFrog Platform
    arg5 : str
        username of the account to preform the replication to target JFrog Platform

    """
    source_url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
        source_url)
    target_url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
        target_url)
    source_header = HEADERS
    target_header = HEADERS
    source_header.update({"Authorization": "Bearer " + source_token})
    target_header.update({"Authorization": "Bearer " + target_token})
    source_response = requests.get(
        source_url + '/artifactory/api/repositories?type=local', headers=source_header, timeout=30)
    logging.debug(source_response.text)
    target_response = requests.get(
        target_url + '/artifactory/api/repositories?type=local', headers=target_header, timeout=30)
    logging.debug(target_response.text)
    for result in literal_eval(source_response.text):
        repo = result.get('key')
        source_config = requests.get(
            source_url + '/artifactory/api/repositories/' + repo, headers=source_header, timeout=30)
        try:
            target_config = requests.put(
                target_url + '/artifactory/api/repositories/' + repo,
                headers=target_header, data=source_config.text, timeout=30)
            target_config.raise_for_status()
        except requests.HTTPError:
            target_config = requests.post(target_url + '/artifactory/api/repositories/' + repo,
                                          headers=target_header,
                                          data=source_config.text, timeout=30)
        data = __setdata(target_url + '/artifactory/' +
                         repo, repo, user, target_token)
        requests.put(source_url + '/artifactory/api/replications/' + repo,
                     headers=source_header, data=data, timeout=30)
        if target_config.ok:
            logging.info(target_config.text)
        else:
            logging.critical(target_config.reason)
            logging.critical(target_config.text)


def sync_remote_repos(source_url, source_token, target_url, target_token):
    """
    This function is intented to compare the remote repos and setup anything missing on the target JFP

    Parameters
    ----------
    arg1 : str
        base URL of the source JFrog Platform
    arg2 : str
        identity token of admin account for the source JFrog Platform
    arg3 : str
        base URL of the target JFrog Platform
    arg4 : str
        identity token of admin account for the target JFrog Platform
    arg5 : str
        username of the account to preform the replication to target JFrog Platform

    """
    source_url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
        source_url)
    target_url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
        target_url)
    source_header = HEADERS
    target_header = HEADERS
    source_header.update({"Authorization": "Bearer " + source_token})
    target_header.update({"Authorization": "Bearer " + target_token})
    source_response = requests.get(
        source_url + '/artifactory/api/repositories?type=remote', headers=source_header, timeout=30)
    logging.debug(source_response.text)
    target_response = requests.get(
        target_url + '/artifactory/api/repositories?type=remote', headers=target_header, timeout=30)
    logging.debug(target_response.text)
    for result in literal_eval(source_response.text):
        repo = result.get('key')
        source_config = requests.get(
            source_url + '/artifactory/api/repositories/' + repo, headers=source_header, timeout=30)
        if __check_offline(source_config):
            logging.warning('%s is offline and will not be migrated', repo)
        else:
            try:
                target_config = requests.put(target_url + '/artifactory/api/repositories/' + repo,
                                             headers=target_header,
                                             data=source_config.text, timeout=30)
                target_config.raise_for_status()
            except requests.HTTPError:
                target_config = requests.post(target_url + '/artifactory/api/repositories/' + repo,
                                              headers=target_header,
                                              data=source_config.text, timeout=30)
            if target_config.ok:
                logging.info(target_config.text)
            else:
                logging.critical(target_config.reason)
                logging.critical(target_config.text)
