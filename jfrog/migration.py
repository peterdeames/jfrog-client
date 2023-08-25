""" functions to enable the migration of JFrog Platform """

import getpass
import json
import logging
from ast import literal_eval
import requests
from tabulate import tabulate

from jfrog import utilities

SOURCE_HEADER = {'content-type': 'application/json'}
TARGET_HEADER = {'content-type': 'application/json'}

# The different levels of logging, from highest urgency to lowest urgency, are:
# CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG
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
    This function is intented to compare the local repos
    and setup anything missing on the target JFP

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
    logging.info("Syncing the local repos from %s to %s",
                 source_url, target_url)
    SOURCE_HEADER.update({"Authorization": "Bearer " + source_token})
    TARGET_HEADER.update({"Authorization": "Bearer " + target_token})
    source_response = requests.get(
        source_url + '/artifactory/api/repositories?type=local', headers=SOURCE_HEADER, timeout=30)
    logging.debug(source_response.text)
    target_response = requests.get(
        target_url + '/artifactory/api/repositories?type=local', headers=TARGET_HEADER, timeout=30)
    logging.debug(target_response.text)
    for result in literal_eval(source_response.text):
        repo = result.get('key')
        source_config = requests.get(
            source_url + '/artifactory/api/repositories/' + repo, headers=SOURCE_HEADER, timeout=30)
        try:
            target_config = requests.put(
                target_url + '/artifactory/api/repositories/' + repo,
                headers=TARGET_HEADER, data=source_config.text, timeout=30)
            target_config.raise_for_status()
        except requests.HTTPError:
            target_config = requests.post(target_url + '/artifactory/api/repositories/' + repo,
                                          headers=TARGET_HEADER,
                                          data=source_config.text, timeout=30)
        data = __setdata(target_url + '/artifactory/' +
                         repo, repo, user, target_token)
        requests.put(source_url + '/artifactory/api/replications/' + repo,
                     headers=SOURCE_HEADER, data=data, timeout=30)
        if target_config.ok:
            logging.info(target_config.text)
        else:
            logging.critical(target_config.reason)
            logging.critical(target_config.text)


def sync_remote_repos(source_url, source_token, target_url, target_token):
    """
    This function is intented to compare the remote repos
    and setup anything missing on the target JFP

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

    """
    source_url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
        source_url)
    target_url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
        target_url)
    logging.info("Syncing the remote repos from %s to %s",
                 source_url, target_url)
    SOURCE_HEADER.update({"Authorization": "Bearer " + source_token})
    TARGET_HEADER.update({"Authorization": "Bearer " + target_token})
    source_response = requests.get(
        source_url + '/artifactory/api/repositories?type=remote', headers=SOURCE_HEADER, timeout=30)
    logging.debug(source_response.text)
    target_response = requests.get(
        target_url + '/artifactory/api/repositories?type=remote', headers=TARGET_HEADER, timeout=30)
    logging.debug(target_response.text)
    for result in literal_eval(source_response.text):
        repo = result.get('key')
        source_config = requests.get(
            source_url + '/artifactory/api/repositories/' + repo, headers=SOURCE_HEADER, timeout=30)
        if __check_offline(source_config):
            logging.warning('%s is offline and will not be migrated', repo)
        else:
            try:
                target_config = requests.put(target_url + '/artifactory/api/repositories/' + repo,
                                             headers=TARGET_HEADER,
                                             data=source_config.text, timeout=30)
                target_config.raise_for_status()
            except requests.HTTPError:
                target_config = requests.post(target_url + '/artifactory/api/repositories/' + repo,
                                              headers=TARGET_HEADER,
                                              data=source_config.text, timeout=30)
            if target_config.ok:
                logging.info(target_config.text)
            else:
                logging.critical(target_config.reason)
                logging.critical(target_config.text)


def sync_permissions(source_url, source_token, target_url, target_token):
    """
    This function is intented to compare the permission
    and setup anything missing on the target JFP

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

    """
    source_url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
        source_url)
    target_url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
        target_url)
    logging.info("Syncing permisions from %s to %s", source_url, target_url)
    SOURCE_HEADER.update({"Authorization": "Bearer " + source_token})
    TARGET_HEADER.update({"Authorization": "Bearer " + target_token})
    target_permisisons = []
    source_response = requests.get(
        source_url + '/artifactory/api/security/permissions', headers=SOURCE_HEADER, timeout=30)
    logging.debug(source_response.text)
    target_response = requests.get(
        target_url + '/artifactory/api/security/permissions', headers=TARGET_HEADER, timeout=30)
    logging.debug(target_response.text)
    for result in literal_eval(target_response.text):
        permission = result.get('name')
        if permission not in target_permisisons:
            target_permisisons.append(permission)
    logging.debug(target_permisisons)
    for result in literal_eval(source_response.text):
        permission = result.get('name')
        source_config = requests.get(source_url +
                                     '/artifactory/api/security/permissions/' + permission,
                                     headers=SOURCE_HEADER, timeout=30)
        target_config = requests.put(target_url +
                                     '/artifactory/api/security/permissions/' + permission,
                                     headers=TARGET_HEADER, data=source_config.text, timeout=30)
        if target_config.ok:
            logging.info(target_config.text)
        else:
            logging.critical(target_config.reason)
            logging.critical(target_config.text)


def check_repos(source_url, source_token, target_url, target_token, rtype):
    """
    This function is intented to compare and report on
    repository differences between 2 JFP Instances

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
        type of repository to compare
        Valid options are: local|remote|virtual

    """
    source_url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
        source_url)
    target_url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
        target_url)
    logging.info("Comparing %s repositories from %s to %s",
                 rtype, source_url, target_url)
    SOURCE_HEADER.update({"Authorization": "Bearer " + source_token})
    TARGET_HEADER.update({"Authorization": "Bearer " + target_token})
    source_count = 0
    target_count = 0
    source_response = requests.get(
        source_url + f'/artifactory/api/repositories?type={rtype}',
        headers=SOURCE_HEADER, timeout=30)
    logging.debug(source_response.text)
    for result in literal_eval(source_response.text):
        source_count = source_count + 1
    logging.debug(source_count)
    target_response = requests.get(
        target_url + f'/artifactory/api/repositories?type={rtype}',
        headers=TARGET_HEADER, timeout=30)
    logging.debug(target_response.text)
    for result in literal_eval(target_response.text):
        target_count = target_count + 1
    logging.debug(target_count)
    if source_count == target_count:
        logging.info('There are %d %s repos setup in the source env and %d %s repos setup in the target env',
                     source_count, rtype, target_count, rtype)
    else:
        logging.error('There are missing %s repos. Source = %d %s repos vs Target = %d %s repos',
                      rtype, source_count, rtype, target_count, rtype)
    logging.info('Checking if repo names match between %s and %s',
                 source_url, target_url)
    for result in literal_eval(source_response.text):
        repo = result.get('key')
        found = False
        for result in literal_eval(target_response.text):
            if repo == result.get('key'):
                found = True
        if not found:
            logging.warning('%s not found in target', repo)
    logging.info('%s repos check complete %s', rtype.title(), '\u2713')
    print('')
