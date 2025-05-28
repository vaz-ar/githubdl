"""
Requests processing module
"""

import json
from logging import getLogger
from os import environ

import requests

from . import url_processing as up

_logger = getLogger('githubdl')


def get_list_of_files_in_path(repo_url: str, base_path: str, reference: str | None) -> dict[str, str]:
    """
    Get the list of files for a given directory path
    """
    _logger.info('Retrieving a list of files for directory: %s', base_path)

    response_object = json.loads(download_git_file_content(repo_url, base_path, reference).decode('utf-8'))

    files = {}

    try:
        for item in response_object:
            files[item.get('name')] = item.get('type')
    except AttributeError as ex:
        err_message = f'Unable to retrieve list of files from response.\n Response: {response_object}'
        _logger.critical(err_message, exc_info=True)
        raise RuntimeError(err_message) from ex
    else:
        return files


def process_request(http_url: str) -> bytes:
    """
    Make the Github API requests
    """
    try:
        response = requests.get(
            # Handle windows and Linux URLs
            url=http_url.replace('\\', '/'),
            headers={
                'Authorization': f'token {environ["GITHUB_TOKEN"]}',
                'Accept': 'application/vnd.github.v3.raw',
            },
            timeout=30,
        )
    except requests.exceptions.RequestException:
        _logger.exception('Error requesting file')
        return b''
    else:
        if response.status_code != 200:
            raise Exception('GET query error!\nmessage: {message}\nStatus code: {status}'.format(**response.json()))

        return response.content


def download_git_file_content(repo_url: str, file_name: str, reference: str | None) -> bytes:
    """
    Download the file content for a given file
    """
    http_url = up.generate_repo_api_url(repo_url, file_name, reference, 'contents')

    _logger.info('Requesting file: %s at url: %s', file_name, http_url)

    return process_request(http_url)


def download_git_repo_info(repo_url: str, info_type: str) -> bytes:
    """
    Download the repo information for a given repo and information type
    """
    http_url = up.generate_repo_api_url(repo_url, None, None, info_type)

    _logger.info('Requesting repository %s  at url: %s', info_type, http_url)

    return process_request(http_url)
