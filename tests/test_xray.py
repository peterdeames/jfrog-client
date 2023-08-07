""" audit unit tests """
from unittest.mock import patch

from jfrog import xray
from nose.tools import assert_equals


@patch('jfrog.xray.requests.get')
def test_xray_ping(mock_post):
    """
    Test ping of xray
    """
    mock_post.status_code = 200
    status = xray.xray_ping('URL', 'TOKEN')
    assert_equals(status, True)
