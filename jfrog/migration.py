""" functions to enable the migration of JFrog Platform """

import json
import logging
from ast import literal_eval
import requests
from tabulate import tabulate
from jfrog import artifactory, utilities

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
    table = []
    t_headers = ['Repo', 'Status']
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
        logging.info('There are %d %s repos setup in the source env and %d %s repos setup in the target env',  # pylint: disable=line-too-long  # noqa: E501
                     source_count, rtype, target_count, rtype)
    else:
        logging.error('There are missing %s repos. Source = %d %s repos vs Target = %d %s repos',
                      rtype, source_count, rtype, target_count, rtype)
    logging.info('Checking if repo names match between %s and %s',
                 source_url, target_url)
    for result in literal_eval(source_response.text):
        repo_lst = []
        repo = result.get('key')
        found = False
        repo_lst.append(repo)
        for result in literal_eval(target_response.text):
            if repo == result.get('key'):
                found = True
                repo_lst.append('OK')
        if not found:
            # logging.warning('%s not found in target', repo)
            repo_lst.append('Missing')
        table.append(repo_lst)
    if len(table) > 0:
        print()
        print(tabulate(table, headers=t_headers))
        print()
        with open(f'{rtype}_repos.txt', 'w', encoding='utf-8') as file:
            file.write(tabulate(table, headers=t_headers))
    logging.info('%s repos check complete %s', rtype.title(), '\u2713')
    print('')


def check_groups(source_url, source_token, target_url, target_token):
    """
    This function is intented to compare and report on
    group differences between 2 JFP Instances

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
    source_version = artifactory.artifactory_version(source_url, source_token)
    target_version = artifactory.artifactory_version(target_url, target_token)
    if utilities.__checkversion(source_version, "7.49.3") and utilities.__checkversion(target_version, "7.49.3"):  # pylint: disable=W0212:protected-access
        table = []
        t_headers = ['Group', 'Status']
        source_url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
            source_url)
        target_url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
            target_url)
        logging.info("Comparing groups from %s to %s", source_url, target_url)
        SOURCE_HEADER.update({"Authorization": "Bearer " + source_token})
        TARGET_HEADER.update({"Authorization": "Bearer " + target_token})
        source_count = 0
        target_count = 0
        source_response = requests.get(source_url + '/access/api/v2/groups',
                                       headers=SOURCE_HEADER, timeout=30)
        logging.debug(source_response.text)
        source_groups = source_response.json()
        source_groups = source_groups['groups']
        source_count = len(source_groups)
        logging.debug(source_count)
        target_response = requests.get(target_url + '/access/api/v2/groups',
                                       headers=TARGET_HEADER, timeout=30)
        logging.debug(target_response.text)
        target_groups = target_response.json()
        target_groups = target_groups['groups']
        target_count = len(target_groups)
        logging.debug(target_count)
        if target_count >= source_count:
            logging.info('There are %d groups in the source env and %d groups in the target env',
                         source_count, target_count)
        else:
            logging.error(
                'There are missing groups. Source = %d groups vs Target = %d groups',
                source_count, target_count)
        for result in source_groups:
            repo_lst = []
            group = result['group_name'].upper()
            found = False
            repo_lst.append(group)
            for result in target_groups:
                if group == result['group_name'].upper():
                    found = True
                    repo_lst.append('OK')
            if not found:
                repo_lst.append('Missing')
                # logging.warning('%s group not found in target', group)
            table.append(repo_lst)
        if len(table) > 0:
            print()
            print(tabulate(table, headers=t_headers))
            print()
            with open('groups.txt', 'w', encoding='utf-8') as file:
                file.write(tabulate(table, headers=t_headers))
        logging.info('Groups check complete %s', '\u2713')
        print('')
    else:
        logging.error(
            "Can't perform the check on groups as one of the versions of artifactory is < 7.49.3")


def check_permissions(source_url, source_token, target_url, target_token):
    """
    This function is intented to compare and report on
    permission differences between 2 JFP Instances

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
    source_version = artifactory.artifactory_version(source_url, source_token)
    target_version = artifactory.artifactory_version(target_url, target_token)
    if utilities.__checkversion(source_version, "6.6.0") and utilities.__checkversion(target_version, "6.6.0"):  # pylint: disable=W0212:protected-access
        table = []
        t_headers = ['Permission', 'Status']
        source_url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
            source_url)
        target_url = utilities.__validate_url(  # pylint: disable=W0212:protected-access
            target_url)
        logging.info("Comparing permissions from %s to %s",
                     source_url, target_url)
        SOURCE_HEADER.update({"Authorization": "Bearer " + source_token})
        TARGET_HEADER.update({"Authorization": "Bearer " + target_token})
        source_count = 0
        target_count = 0
        source_response = requests.get(source_url + '/artifactory/api/security/permissions',
                                       headers=SOURCE_HEADER, timeout=30)
        logging.debug(source_response.text)
        source_permissions = source_response.json()
        source_count = len(source_permissions)
        logging.debug(source_count)
        target_response = requests.get(target_url + '/artifactory/api/security/permissions',
                                       headers=TARGET_HEADER, timeout=30)
        logging.debug(target_response.text)
        target_permissions = target_response.json()
        target_count = len(target_permissions)
        logging.debug(target_count)
        if target_count >= source_count:
            logging.error(
                'There are missing permissions.  Source = %d permissions vs Target = %d permissions',
                source_count, target_count)
        else:
            logging.info('There are %d permissions in the source env and %d permissions in the target env',
                         source_count, target_count)
        for result in literal_eval(source_response.text):
            repo_lst = []
            permission = result.get('name')
            found = False
            repo_lst.append(permission)
            for result in literal_eval(target_response.text):
                if permission.upper() == result.get('name').upper():
                    found = True
                    repo_lst.append('OK')
            if not found:
                repo_lst.append('Missing')
                # logging.warning('%s permission not found in target', permission)
            table.append(repo_lst)
        if len(table) > 0:
            print()
            print(tabulate(table, headers=t_headers))
            print()
            with open('permissions.txt', 'w', encoding='utf-8') as file:
                file.write(tabulate(table, headers=t_headers))
        logging.info('Permissions check complete %s', '\u2713')
        print('')
    else:
        logging.error(
            "Can't perform the check on permissions as one of the versions of artifactory is < 6.6.0")  # pylint: disable=line-too-long  # noqa: E501


def check_artifacts(source_url, source_token, target_url, target_token):
    """
    This function is intented to compare and report on
    artifact differences between 2 JFP Instances

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
    SOURCE_HEADER.update({"Authorization": "Bearer " + source_token})
    TARGET_HEADER.update({"Authorization": "Bearer " + target_token})
    logging.info("Recalculating storage on %s and %s",
                 source_url, target_url)
    logging.info("This may take up to 2 mins..")
    # requests.post(source_url + '/artifactory/api/storageinfo/calculate',
    #              headers=SOURCE_HEADER, timeout=30)
    # requests.post(target_url + '/artifactory/api/storageinfo/calculate',
    #              headers=TARGET_HEADER, timeout=30)
    utilities.__progressbar(100)  # pylint: disable=W0212:protected-access
    logging.info("Comparing artifacts from %s to %s",
                 source_url, target_url)
    source_response = requests.get(source_url + '/artifactory/api/storageinfo',
                                   headers=SOURCE_HEADER, timeout=30)
    target_response = requests.get(target_url + '/artifactory/api/storageinfo',
                                   headers=TARGET_HEADER, timeout=30)
    table = []
    t_headers = ['Repo', 'Repo Type', 'Source Count', 'Target Count']
    for sresult in literal_eval(source_response.text)["repositoriesSummaryList"]:
        repo_lst = []
        repo = sresult.get('repoKey')
        rtype = sresult.get('repoType')
        source_count = sresult.get('filesCount')
        if rtype != 'REMOTE' and rtype != 'NA' and repo != 'jfrog-usage-logs':
            repo_lst.append(repo)
            repo_lst.append(rtype)
            repo_lst.append(source_count)
            for tresult in literal_eval(target_response.text)["repositoriesSummaryList"]:
                if tresult.get('repoKey') == repo:
                    target_count = tresult.get('filesCount')
                    repo_lst.append(target_count)
                    if source_count != target_count:
                        if source_count > target_count:
                            diff = source_count - target_count
                            if diff >= 1000:
                                logging.critical(
                                    'There are differences in artifact counts in %s.  Source = %d items vs Target = %d items (%d items)',  # pylint: disable=line-too-long  # noqa: E501
                                    repo, source_count, target_count, diff)
                            elif diff >= 100:
                                logging.error(
                                    'There are differences in artifact counts in %s.  Source = %d items vs Target = %d items (%d items)',  # pylint: disable=line-too-long  # noqa: E501
                                    repo, source_count, target_count, diff)
                            else:
                                logging.warning(
                                    'There are differences in artifact counts in %s.  Source = %d items vs Target = %d items (%d items)',  # pylint: disable=line-too-long  # noqa: E501
                                    repo, source_count, target_count, diff)

                        else:
                            logging.info(
                                'There are differences in artifact counts in %s.  Source = %d items vs Target = %d items',  # pylint: disable=line-too-long  # noqa: E501
                                repo, source_count, target_count)
                    table.append(repo_lst)
                    break
    stotalartifacts = source_response.json()
    stotalartifacts = stotalartifacts['binariesSummary']['artifactsCount']
    ttotalartifacts = target_response.json()
    ttotalartifacts = ttotalartifacts['binariesSummary']['artifactsCount']
    logging.info('There are %s artifacts in %s and %s artifacts in %s',
                 stotalartifacts, source_url, ttotalartifacts, target_url)
    if len(table) > 0:
        print()
        print(tabulate(table, headers=t_headers))
        print()
        with open('artifacts.txt', 'w', encoding='utf-8') as file:
            file.write(tabulate(table, headers=t_headers))
    logging.info('Artifact check complete %s', '\u2713')
    print('')
