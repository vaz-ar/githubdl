"""
Requests processing module
"""

import json
import os
from logging import getLogger
from os import environ
from typing import Any

import requests

from . import url_processing as up


_logger = getLogger('githubdl')


def get_files_from_json(response_object: dict[Any, Any]) -> dict[str, str]:
    files = {}
    try:
        for item in response_object:
            files.update({item.get('name'): item.get('type')})
    except AttributeError as ex:
        err_message = (
            'Unable to retrieve list of files from response.\n Exception: '
            + str(ex)
            + '\n Response: '
            + str(response_object)
        )
        _logger.critical(err_message)
        raise RuntimeError(err_message) from ex
    else:
        return files


def get_list_of_files_in_path(repo_url: str, base_path: str, reference: str) -> dict[str, str]:
    _logger.info('Retrieving a list of files for directory: %s', base_path)
    response = download_git_file_content(repo_url, base_path, reference)
    response_object = json.loads(response.decode('utf-8'))
    return get_files_from_json(response_object)


def process_request(http_url: str) -> bytes:
    try:
        request = requests.get(
            url=fix_url_path_on_windows(http_url),
            headers={
                'Authorization': f'token {environ["GITHUB_TOKEN"]}',
                'Accept': 'application/vnd.github.v3.raw',
            },
            timeout=30,
        )
    except requests.exceptions.RequestException:
        _logger.exception('Error requesting file')
    else:
        return request.content


def fix_url_path_on_windows(http_url: str) -> str:
    if os.name == 'nt':
        return http_url.replace('\\', '/')
    return http_url


def download_git_file_content(repo_url: str, file_name: str, reference: str) -> bytes:
    (domain_name, repo_name) = up.get_url_components(repo_url)
    http_url = up.generate_repo_api_url(domain_name, repo_name, file_name, reference, 'contents')
    _logger.info('Requesting file: %s at url: %s', file_name, http_url)
    return process_request(http_url)


def download_git_repo_info(repo_url: str, info_type: str) -> bytes:
    (domain_name, repo_name) = up.get_url_components(repo_url)
    http_url = up.generate_repo_api_url(domain_name, repo_name, '', '', info_type)
    _logger.info('Requesting repository %s  at url: %s', info_type, http_url)
    return process_request(http_url)
