import json
import logging
import requests
from io import StringIO
from typing import Union

from ._core import load_api_key, get_api_url, assemble_headers


def list_voices(api_key: str = None, api_url: str = None, insecure: bool = False, details: bool = False,
                output: Union[str, StringIO] = None, logger: logging.Logger = None) -> bool:
    """
    Lists the available voices.

    :param api_key: the API key to use (if necessary)
    :type api_key: str or None
    :param api_url: the API URL to use
    :type api_url: str or None
    :param insecure: whether to turn off the SSL certificate check, e.g., when using self-signed certs
    :type insecure: bool
    :param details: whether to output all the details or just the voices
    :type details: bool
    :param output: the file or StringIO to store the result in, uses stdout if None
    :type output: str or StringIO or None
    :param logger: the optional logger to use for outputting information
    :type logger: logging.Logger
    :return: True if successfully queried
    :rtype: bool
    """
    # headers
    headers = assemble_headers(api_key=api_key, logger=logger)

    # build URL
    url = get_api_url(api_url=api_url, logger=logger)
    if not url.endswith("/"):
        url += "/"
    url += "voices"
    if logger is not None:
        logger.info("Listing voices using: %s" % url)

    # perform request
    r = requests.get(url, headers=headers, verify=not insecure)
    if r.status_code != 200:
        if logger is not None:
            logger.error("Request failed with status code: %d" % r.status_code)
        return False

    try:
        d = r.json()
        # all of it or just voice names?
        if details:
            data = d
        else:
            data = list(d.keys())
        if output is None:
            print(json.dumps(data, indent=2))
        elif isinstance(output, str):
            with open(output, "w") as fp:
                json.dump(data, fp, indent=2)
        elif isinstance(output, StringIO):
            json.dump(data, output, indent=2)
        else:
            raise Exception("Unsupported output type: %s" % str(type(output)))
    except:
        if logger is not None:
            logger.exception("Failed to parse result as JSON: %s" % r.text)

    return True

