"""
Files processing module
"""

import os
import pathlib
from logging import getLogger

_logger = getLogger('githubdl')


def get_target_full_filename(file_name: str, target_path: str) -> str:
    """
    Return full filename
    """
    modified_path = get_filename_without_first_directory(file_name)
    return os.path.join(target_path, modified_path)


def get_filename_without_first_directory(file_name: str) -> str:
    path = pathlib.Path(file_name)
    return str(pathlib.Path(*path.parts[1:]))


def write_file(file_name: str, file_data: bytes) -> None:
    _logger.info('Writing to file: %s', file_name)
    with open(file_name, 'wb') as write_file:
        write_file.write(file_data)


def create_directory(dir_name: str) -> None:
    _logger.info('Checking for directory: %s', dir_name)
    if not os.path.exists(dir_name):
        _logger.info('Creating directory: %s', dir_name)
        os.makedirs(dir_name)
