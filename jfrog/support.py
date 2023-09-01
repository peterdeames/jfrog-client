""" functions to manage support actions """

import json
import logging

import requests
from tqdm import tqdm

from jfrog import utilities

HEADERS = {'content-type': 'application/json'}

# The different levels of logging, from highest urgency to lowest urgency, are:
# CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


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
