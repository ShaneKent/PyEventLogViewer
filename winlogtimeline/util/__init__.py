import os


def get_package_data_path(file_path, *package_data):
    """
    Used for retrieving package data from within the associated package.
    :param file_path: Should be __file__ (passed from within the appropriate module).
    :param package_data: Arguments representing the path to the data file from within the module.
    :return: The absolute path to the data file.
    """
    dir_name, file_name = os.path.split(file_path)
    data_path = os.path.join(dir_name, *package_data)
    return data_path
