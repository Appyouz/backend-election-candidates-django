"""
This file is used in settings/core.py for required checks.
"""

import os
from decouple import config
from decouple import Config, RepositoryEnv


def raise_if_debug_not_properly_set():
    """
    Raise ValueError if DJANGO_DEBUG is not set.

    :raises ValueError: DJANGO_DEBUG not set. Set it using `export DJANGO_DEBUG=True`(or False). See more in README, search for `DJANGO_DEBUG`
    """
    debug = os.environ.get("DJANGO_DEBUG")
    if debug is None:
        raise ValueError(
            "DJANGO_DEBUG not set. Set it using `export DJANGO_DEBUG=True`(or False). See more in README, search for `DJANGO_DEBUG`"
        )

    if debug not in ["True", "False"]:
        raise ValueError(
            "DJANGO_DEBUG should be True or False. Set it using `export DJANGO_DEBUG=True`(or False). See more in README, search for `DJANGO_DEBUG`. Note the capitalization."
        )


def raise_if_env_not_found(debug: bool):
    """
    Raise FileNotFoundError if .env file does not exist.

    :raises FileNotFoundError: Config file .env not found.
    """

    env_file = ".env" if debug else ".env.prod"

    print(debug, env_file)

    if not os.path.exists(env_file):
        raise FileNotFoundError(
            f"Config file {env_file} not found. Create it to continue. You've set DJANGO_DEBUG to {debug}, so the file should be {env_file}"
        )


def get_config(debug: bool):
    """
    Load config file based on DEBUG value in settings.

    :param debug: DEBUG value in settings, defaults to False
    :return: decouple.Config instance choosing .env or .env.prod by the DEBUG value
    :rtype: decouple.Config
    """

    config_file = ".env" if debug else ".env.prod"
    config = Config(RepositoryEnv(config_file))

    return config


def check_all_okay():

    raise_if_debug_not_properly_set()
    debug_str = os.environ.get("DJANGO_DEBUG")
    # we can be sure that debug_str is "True" or "False" cause raise_if_debug_not_properly_set() validates that as well
    debug = True if debug_str == "True" else False
    raise_if_env_not_found(debug=debug)
