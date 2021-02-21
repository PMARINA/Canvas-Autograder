"""Encapsulation for requests library to handle the header, since all Canvas API calls must include the token in the header."""
import requests

import Token
import Variables

baseurl = f"https://{Variables.DOMAIN}.instructure.com"
baseurl_apiv1 = f"{baseurl}/api/v1"
headers = {"Authorization": f"Bearer {Token.get()}"}


def get_endpoint(endpoint: str) -> requests.Response:
    """Return a response from a canvas endpoint given urlquery.

    Args:
        endpoint (str): The specific urlquery

    Returns:
        requests.Response: The response from that query
    """
    get_url = "/".join([baseurl_apiv1, endpoint])
    assert baseurl.startswith("https")
    response = requests.get(get_url, headers=headers)
    return response


def get(url: str) -> requests.Response:
    """Perform a get request with required headers for canvas (do not use for other sites).

    Args:
        url (str): The url you wish to query

    Returns:
        requests.Response: The response object from the query
    """
    assert url.startswith("https")
    response = requests.get(url, headers=headers)
    return response
