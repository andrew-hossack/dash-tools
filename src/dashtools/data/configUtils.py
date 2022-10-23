'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-05-28 13:56:14
'''

import configparser
from typing import List, Union


def _get_config() -> List[str]:
    """
    Get the config file
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def get_config_value(key: str, section: str = "DEFAULT") -> Union[str, None]:
    """
    Get the value of a key in a section or None if not found
    """
    config = _get_config()
    try:
        value = config[section][key]
        if len(value) > 0:
            return value
        return None
    except KeyError:
        return None


def set_config_value(key: str, value: str, section: str = "DEFAULT") -> None:
    """
    Set the value of a key in a section
    """
    config = _get_config()
    config.set(section, key, value)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
