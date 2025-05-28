"""
Files processing module
"""

from logging import getLogger
from pathlib import Path


_logger = getLogger('githubdl')


def write_file(file_name: Path, file_data: bytes) -> None:
    """
    Write file content to disk
    """
    _logger.info('Writing to file: %s', file_name)
    file_name.write_bytes(file_data)


def create_directory(dir_name: Path) -> None:
    """
    Create local directory on disk
    """
    _logger.info('Checking for directory: %s', dir_name)
    if not dir_name.exists():
        _logger.info('Creating directory: %s', dir_name)
        dir_name.mkdir(parents=True, exist_ok=True)
