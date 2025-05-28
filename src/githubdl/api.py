"""
API module

Exposed methods for the githubdl library
"""

import re
from json import loads as json_loads
from logging import getLogger
from pathlib import Path

from . import file_processing as fp
from . import request_processing as rp


_logger = getLogger('githubdl')


def dl_info(repo_url: str, info_type: str) -> str:
    """
    Download github repository information
    """
    return json_loads(rp.download_git_repo_info(repo_url, info_type).decode('utf-8'))


def dl_file(
    repo_url: str,
    file_name: str,
    target_filename: str | None = None,
    reference: str | None = None,
) -> None:
    """
    Download a specific file
    """
    dest = Path(file_name).name if target_filename is None else target_filename

    fp.write_file(
        Path(dest),
        rp.download_git_file_content(repo_url, file_name, reference),
    )


def dl_dir(
    repo_url: str,
    base_path: str,
    target_path: str | None = None,
    reference: str | None = None,
    submodules: bool = False,
) -> None:
    """
    Download a specific directory
    """
    files = rp.get_list_of_files_in_path(repo_url, base_path, reference)

    for file_item, file_type in files.items():
        if file_type == 'dir':
            dl_dir(
                repo_url=repo_url,
                base_path=str(Path(base_path) / file_item),
                target_path=target_path,
            )
        else:
            download_filename = str(Path(base_path, file_item)).removeprefix('/')
            file_content = rp.download_git_file_content(repo_url, download_filename, reference)

            if target_path is None:
                target_path = '.'

            full_file_name = Path(target_path, download_filename)

            fp.create_directory(full_file_name.parent)

            fp.write_file(full_file_name, file_content)

            if submodules and file_item.lower().endswith('.gitmodules'):
                process_gitmodule(
                    target_path,
                    str(full_file_name),
                )


def process_gitmodule(target_path: str, full_filename: str) -> None:
    """
    Process git sub modules
    """
    with Path(full_filename).open(encoding='utf-8') as f:
        content = [x.strip() for x in f]

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
            tmp_path = Path(target_path) / path.group(1)
            tmp_url = url.group(1)
            path = url = None
            fp.create_directory(tmp_path)
            dl_dir(
                repo_url=tmp_url,
                base_path='/',
                target_path=str(tmp_path),
                submodules=True,
            )


def dl_tags(repo_url: str) -> str:
    """
    Download the list of tags for the repo
    """
    return dl_info(repo_url, 'tags')


def dl_branches(repo_url: str) -> str:
    """
    Download the list of branches for the repo
    """
    return dl_info(repo_url, 'branches')
