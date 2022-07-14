import requests

from coins.services.api_calls import get_ping


def test_ping_status_is_200():
    res: requests.Response = get_ping()
    assert res.status_code == 200
    
    