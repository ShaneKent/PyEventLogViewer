import json
import os


def get_package_data_path(file_path, *package_data_path):
    """
    Used for retrieving package data from within the associated package.
    :param file_path: Should be __file__ (passed from within the appropriate module).
    :param package_data_path: Arguments representing the path to the data file from within the module.
    :return: The absolute path to the data file.
    """
    dir_name, file_name = os.path.split(file_path)
    data_path = os.path.join(dir_name, *package_data_path)
    return data_path


def open_config():
    """
    Helper method for accessing the config.
    :return: Returns a dictionary matching the structure of config/config.json.
    """
    config_path = get_package_data_path(__file__, 'config', 'config.json')

    with open(config_path) as config_file:
        config = json.load(config_file)

    return config
