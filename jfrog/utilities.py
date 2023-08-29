""" shared functions to manage JFrog Platform """
import json
import logging
import sys
import time

from packaging import version

# The different levels of logging, from highest urgency to lowest urgency, are:
# CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


def __progressbar(duration):
    """ prints a progress bar on screen """
    toolbar_width = duration

    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    # return to start of line, after '['
    sys.stdout.write("\b" * (toolbar_width+1))

    for _ in range(toolbar_width):
        time.sleep(1)  # do real work here
        # update the bar
        sys.stdout.write("#")
        sys.stdout.flush()

    sys.stdout.write("]\n")  # this ends the progress bar


def __checkversion(current_version, lowest_version):
    """ compares 2 versions to check current is higher than lowest """
    check = version.parse(current_version) > version.parse(lowest_version)
    return check


def __get_msg(response, rtype):
    """ gets the message test from a response """
    rmessage = response.json()
    rmessage = rmessage[rtype]
    rmessage = rmessage[0]['message']
    return rmessage


def __validate_url(url):
    updateurl = 'You should update the base url.'
    url = url.strip()
    if url.lower().endswith('/'):
        logging.warning(
            "Found a / at the end of the URL this has been removed.")
        logging.warning(updateurl)
        url = url.strip("/")
    if url.lower().endswith('/artifactory'):
        logging.warning(
            "Found /artifactory at the end of the URL this has been removed.")
        logging.warning(updateurl)
        url = url.strip("/artifactory")
    if url.lower().endswith('/xray'):
        logging.warning(
            "Found /xray at the end of the URL this has been removed.")
        logging.warning(updateurl)
        url = url.strip("/xray")
    if url.lower().endswith('/mc'):
        logging.warning(
            "Found /mc at the end of the URL this has been removed.")
        logging.warning(updateurl)
        url = url.strip("/mc")
    return url


def __set_repo_data(name, layout, ptype, rtype):
    """ This function sets the data to be sent for the creation of a repo """
    data = {}
    data["key"] = name
    data["rclass"] = rtype
    data["packageType"] = ptype
    data["xrayIndex"] = 'true'
    data["repoLayoutRef"] = layout
    data = json.dumps(data)
    return data


def __set_token_data(description, scope, expires_in, refreshable, username, project_key):
    """ This function sets the data to be sent for the creation of a token """
    data = {}
    if description is not None:
        data["description"] = description
    if scope is not None:
        data["scope"] = scope
    if expires_in is not None and expires_in > 0:
        data["expires_in"] = expires_in
    if refreshable:
        data["refreshable"] = refreshable
    if scope is not None:
        data["username"] = username
    if project_key is not None:
        data["project_key"] = project_key
    data["include_reference_token"] = True
    data = json.dumps(data)
    return data


def __setlayout(ptype):
    ''' Choose the correct default layout based on the repository type '''
    specialtypes = ['bower', 'cargo', 'composer', 'conan', 'go', 'ivy',
                    'npm', 'nuget', 'puppet', 'sbt', 'swift', 'vcs']
    if ptype.lower() in ['maven', 'gradle']:
        return 'maven-2-default'
    if ptype.lower() in specialtypes:
        return ptype.lower() + '-default'
    return 'simple-default'
