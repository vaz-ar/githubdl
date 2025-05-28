"""
File download tests
"""

from collections.abc import Generator
from os import environ
from pathlib import Path
from shutil import rmtree
from typing import Any

import pytest

import githubdl

# ruff: noqa: S101
# ruff: noqa: ANN001


files_list = [
    {
        'src': 'Cargo.toml',
        'target': None,
        'expected_path': 'Cargo.toml',
    },
    {
        'src': 'Cargo.toml',
        'target': 'tmp_files/my_dir/renamed_Cargo.toml',
        'expected_path': 'tmp_files/my_dir/renamed_Cargo.toml',
    },
    {
        'src': '.cargo/config.toml',
        'target': None,
        'expected_path': 'config.toml',
    },
    {
        'src': '.cargo/config.toml',
        'target': 'tmp_files/my_dir/config.toml',
        'expected_path': 'tmp_files/my_dir/config.toml',
    },
]

directories_list = [
    {
        'src': 'xtask',
        'target': None,
        'expected_paths': {
            'dirs': [
                'xtask',
                'xtask/src',
            ],
            'files': [
                'xtask/src/build.rs',
                'xtask/src/ci.rs',
                'xtask/src/clippy.rs',
                'xtask/src/dist.rs',
                'xtask/src/flags.rs',
                'xtask/src/format.rs',
                'xtask/src/main.rs',
                'xtask/src/pipelines.rs',
                'xtask/src/test.rs',
                'xtask/Cargo.toml',
            ],
        },
    },
    {
        'src': 'xtask',
        'target': 'tmp_dir_1',
        'expected_paths': {
            'dirs': [
                'tmp_dir_1/xtask',
                'tmp_dir_1/xtask/src',
            ],
            'files': [
                'tmp_dir_1/xtask/src/build.rs',
                'tmp_dir_1/xtask/src/ci.rs',
                'tmp_dir_1/xtask/src/clippy.rs',
                'tmp_dir_1/xtask/src/dist.rs',
                'tmp_dir_1/xtask/src/flags.rs',
                'tmp_dir_1/xtask/src/format.rs',
                'tmp_dir_1/xtask/src/main.rs',
                'tmp_dir_1/xtask/src/pipelines.rs',
                'tmp_dir_1/xtask/src/test.rs',
                'tmp_dir_1/xtask/Cargo.toml',
            ],
        },
    },
    {
        'src': 'xtask',
        'target': 'tmp_dir_2/2',
        'expected_paths': {
            'dirs': [
                'tmp_dir_2/2/xtask',
                'tmp_dir_2/2/xtask/src',
            ],
            'files': [
                'tmp_dir_2/2/xtask/src/build.rs',
                'tmp_dir_2/2/xtask/src/ci.rs',
                'tmp_dir_2/2/xtask/src/clippy.rs',
                'tmp_dir_2/2/xtask/src/dist.rs',
                'tmp_dir_2/2/xtask/src/flags.rs',
                'tmp_dir_2/2/xtask/src/format.rs',
                'tmp_dir_2/2/xtask/src/main.rs',
                'tmp_dir_2/2/xtask/src/pipelines.rs',
                'tmp_dir_2/2/xtask/src/test.rs',
                'tmp_dir_2/2/xtask/Cargo.toml',
            ],
        },
    },
    {
        'src': 'xtask/src',
        'target': None,
        'expected_paths': {
            'dirs': [
                'xtask/src',
            ],
            'files': [
                'xtask/src/build.rs',
                'xtask/src/ci.rs',
                'xtask/src/clippy.rs',
                'xtask/src/dist.rs',
                'xtask/src/flags.rs',
                'xtask/src/format.rs',
                'xtask/src/main.rs',
                'xtask/src/pipelines.rs',
                'xtask/src/test.rs',
            ],
        },
    },
    {
        'src': 'xtask/src',
        'target': 'tmp_dir_4/2/3/4',
        'expected_paths': {
            'dirs': [
                'tmp_dir_4/2/3/4/xtask',
                'tmp_dir_4/2/3/4/xtask/src',
            ],
            'files': [
                'tmp_dir_4/2/3/4/xtask/src/build.rs',
                'tmp_dir_4/2/3/4/xtask/src/ci.rs',
                'tmp_dir_4/2/3/4/xtask/src/clippy.rs',
                'tmp_dir_4/2/3/4/xtask/src/dist.rs',
                'tmp_dir_4/2/3/4/xtask/src/flags.rs',
                'tmp_dir_4/2/3/4/xtask/src/format.rs',
                'tmp_dir_4/2/3/4/xtask/src/main.rs',
                'tmp_dir_4/2/3/4/xtask/src/pipelines.rs',
                'tmp_dir_4/2/3/4/xtask/src/test.rs',
            ],
        },
    },
]


@pytest.fixture(params=directories_list, scope='function')
def directory_info(request) -> Generator[dict[str, str], Any, None]:
    """
    Parametric fixture that return the directory information
    """
    if request.param['target'] is not None:
        target = Path(request.param['target'])
        if target.exists():
            target.rmdir()

    yield request.param

    for x in request.param['expected_paths']['files']:
        x_path = Path(x)
        if x_path.exists() and x_path.is_file():
            x_path.unlink()

    for x in reversed(request.param['expected_paths']['dirs']):
        x_path = Path(x)
        if x_path.exists() and x_path.is_dir():
            x_path.rmdir()

    if request.param['target'] is not None:
        target.rmdir()


@pytest.fixture(params=files_list)
def file_info(request) -> Generator[dict[str, str], Any, None]:
    """
    Parametric fixture that return the file information

    It creates the parent directory for the file during the setup phase,
    then delete the file during the teardown
    """
    Path(request.param['expected_path']).parent.mkdir(parents=True, exist_ok=True)

    yield request.param

    loc_path = Path(request.param['expected_path'])
    if loc_path.exists() and loc_path.is_file():
        loc_path.unlink()


def test_github_token() -> None:
    """
    Test if the github token has been set
    """
    assert environ.get('GITHUB_TOKEN', '')


def test_file_download_correct_path(file_info) -> None:
    """
    Test download files
    """
    githubdl.dl_file(
        repo_url='https://github.com/zellij-org/zellij',
        file_name=file_info['src'],
        target_filename=file_info['target'],
    )

    path_obj = Path(file_info['expected_path'])
    assert path_obj.is_file()
    assert path_obj.stat().st_size > 0


def test_directory_download_correct_path(directory_info) -> None:
    """
    Test download directories
    """
    githubdl.dl_dir(
        repo_url='https://github.com/zellij-org/zellij',
        base_path=directory_info['src'],
        target_path=directory_info['target'],
    )

    for x in directory_info['expected_paths']['dirs']:
        x_path = Path(x)
        assert x_path.exists()
        assert x_path.is_dir()

    for x in directory_info['expected_paths']['files']:
        x_path = Path(x)
        assert x_path.exists()
        assert x_path.is_file()
