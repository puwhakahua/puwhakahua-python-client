import logging
import os
from typing import Dict, Optional

ENV_PUWHAKAHUA_LOGLEVEL = "PUWHAKAHUA_LOGLEVEL"
""" environment variable for specifying the log level. """

ENV_PUWHAKAHUA_API_KEY = "PUWHAKAHUA_API_KEY"
""" environment variable for the API key (if not loaded from file). """

ENV_PUWHAKAHUA_API_URL = "PUWHAKAHUA_API_URL"
""" environment variable for the API endpoint URL. """

DEFAULT_API_URL = "https://api.puwhakahua.nz"
""" the default URL for the api. """


def load_api_key(api_key: str = None, logger: logging.Logger = None) -> str:
    """
    Loads the API key from the specified file or from the environment variable.

    :param api_key: the file to load the key from instead of obtaining it from the environment variable
    :type api_key: str
    :param logger: the optional logger for outputting information
    :type logger: logging.Logger
    :return: the key or None if not specified/necessary
    :rtype: str or None
    """
    result = None
    if api_key is None:
        if ENV_PUWHAKAHUA_API_KEY in os.environ:
            if logger is not None:
                logger.info("Obtaining API key from: %s" % ENV_PUWHAKAHUA_API_KEY)
            result = os.environ[ENV_PUWHAKAHUA_API_KEY]
    else:
        if not os.path.exists(api_key):
            raise Exception("API key file does not exist: %s" % api_key)
        if os.path.isdir(api_key):
            raise Exception("API key file points to a directory: %s" % api_key)
        if logger is not None:
            logger.info("Loading API key from: %s" % api_key)
        with open(api_key, "r") as fp:
            result = fp.readline()
    if result is not None:
        result = result.strip()
        if len(result) < 32:
            raise Exception("Unexpected length of API key: %d" % len(result))
    if result is None and (logger is not None):
        logger.info("No API key determined")
    return result


def assemble_headers(api_key: str = None, logger: logging.Logger = None) -> Optional[Dict[str, str]]:
    """
    Assembles the headers for API requests.

    :param api_key: the API key to use (if necessary)
    :type api_key: str or None
    :param logger: the optional logger to use for outputting information
    :type logger: logging.Logger
    :return: the generated headers or None if not necessary
    """
    key = load_api_key(api_key, logger=logger)
    if key is None:
        result = None
    else:
        result = {"x-api-key": key}
    return result


def get_api_url(api_url: str = None, logger: logging.Logger = None) -> str:
    """
    Returns the API endpoint URL.
    Takes the PUWHAKAHUA_API_URL environment variable into account.

    :param api_url: an optional API URL to override the default or environment variable
    :type api_url: str or None
    :param logger: the optional logger to use
    :type logger: logging.Logger
    :return: the URL for the API
    :rtype: str
    """
    if api_url is not None:
        if logger is not None:
            logger.info("Using custom URL")
        result = api_url
    elif ENV_PUWHAKAHUA_API_URL in os.environ:
        if logger is not None:
            logger.info("Using URL from %s environment variable" % ENV_PUWHAKAHUA_API_URL)
        result = os.environ[ENV_PUWHAKAHUA_API_URL]
    else:
        if logger is not None:
            logger.info("Using default API URL")
        result = DEFAULT_API_URL
    if logger is not None:
        logger.info("Using API URL: %s" % result)
    return result
