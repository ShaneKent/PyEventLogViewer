import json
import os
import appdirs
import shutil


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
    # Get the path to the default config file
    config_template_path = get_package_data_path(__file__, 'config', 'config.json')

    # Get the path to the working config file
    config_folder_path = get_appdir()
    config_path = os.path.join(config_folder_path, 'config.json')

    # Make sure that the config directory exists
    if not os.path.exists(config_folder_path):
        os.makedirs(config_folder_path)

    # Copy the config file to the application data directory. This allows for user edits in
    # a non-elevated context, and allows us to keep a default version of the config.
    if not os.path.isfile(config_path):
        shutil.copy(config_template_path, config_folder_path)

    with open(config_path) as config_file:
        config = json.load(config_file)

    return config


def write_config(data):
    """
    Helper method for writing to the config
    :return:
    """
    # Get the path to the default config file
    config_template_path = get_package_data_path(__file__, 'config', 'config.json')

    # Get the path to the working config file
    config_path = os.path.join(get_appdir(), 'config.json')

    # Copy the config file to the application data directory. This allows for user edits in
    # a non-elevated context, and allows us to keep a default version of the config.
    if not os.path.isfile(config_path):
        shutil.copy2(config_template_path, config_path)

    with open(config_path, "w") as config_file:
        json.dump(data, config_file)

    return



def get_appdir():
    """
    Helper method for accessing the application directory.
    :return:
    """
    return appdirs.user_data_dir('PyEventLogTimeline', 'Redacted')
