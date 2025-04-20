"""
API module

Exposed methods for the githubdl library
"""

import os
import re
from logging import getLogger

from . import file_processing as fp
from . import request_processing as rp
from . import url_processing as up

_logger = getLogger('githubdl')


def set_default_if_empty(variable_to_check: str, default_value: str) -> str:
    if not variable_to_check:
        return default_value
    return variable_to_check


def save_file_to_path(repo_url: str, download_filename: str, target_path: str, reference: str) -> None:
    download_file = rp.download_git_file_content(repo_url, download_filename, reference)
    full_file_name = fp.get_target_full_filename(download_filename, target_path)
    full_dir_name, _ = os.path.split(full_file_name)
    fp.create_directory(full_dir_name)
    fp.write_file(full_file_name, download_file)


def dl_info(repo_url: str, info_type: str) -> str:
    tags = rp.download_git_repo_info(repo_url, info_type)
    return tags.decode('utf-8')


#  -----------------------------------------------------------------------------
# Exposed api methods below


def dl_file(
    repo_url: str,
    file_name: str,
    target_filename: str = '',
    reference: str = '',
) -> None:
    target_filename = set_default_if_empty(target_filename, file_name)
    file_data = rp.download_git_file_content(repo_url, file_name, reference)
    fp.write_file(target_filename, file_data)


def dl_dir(
    repo_url: str,
    base_path: str,
    target_path: str = '',
    reference: str = '',
    submodules: str = '',
) -> None:
    target_path = set_default_if_empty(target_path, base_path)
    files = rp.get_list_of_files_in_path(repo_url, base_path, reference)
    for file_item, file_type in files.items():
        if file_type == 'dir':
            recurse_dir = os.path.join(base_path, file_item)
            dl_dir(repo_url, recurse_dir, target_path)
        else:
            download_filename = os.path.join(base_path, file_item)
            save_file_to_path(repo_url, download_filename, target_path, reference)
            if file_item.lower().endswith('.gitmodules') and submodules:
                full_filename = fp.get_target_full_filename(download_filename, target_path)
                process_gitmodule(target_path, full_filename)


def process_gitmodule(target_path: str, full_filename: str) -> None:
    with open(full_filename, encoding='utf-8') as f:
        content = f.readlines()

    content = [x.strip() for x in content]
    path = None
    url = None
    path_pred = re.compile(r'^\s*path\s*=\s*(.*)$')
    url_pred = re.compile(r'^\s*url\s*=\s*(.*)$')

    for line in content:
        if not path:
            path = path_pred.search(line)
        if not url:
            url = url_pred.search(line)
        if path and url:
            tmp_path = os.path.join(target_path, path.group(1))
            tmp_url = url.group(1)
            path = url = None
            fp.create_directory(tmp_path)
            dl_dir(repo_url=tmp_url, base_path='/', target_path=tmp_path, submodules=True)


def dl_tags(repo_url: str) -> str:
    return dl_info(repo_url, 'tags')


def dl_branches(repo_url: str) -> str:
    return dl_info(repo_url, 'branches')


def get_repo_name_from_url(repo_url: str) -> str:
    _, repo_name = up.get_url_components(repo_url)
    return repo_name


def get_domain_name_from_url(repo_url: str) -> str:
    domain_name, _ = up.get_url_components(repo_url)
    return domain_name
