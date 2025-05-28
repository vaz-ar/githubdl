"""
API related tests
"""

from collections.abc import Generator
from pathlib import Path
from shutil import rmtree
from typing import Any

import pytest

import githubdl

# ruff: noqa: D401
# ruff: noqa: S101
# ruff: noqa: ANN001


@pytest.fixture
def path_file_str() -> Generator[str, Any, None]:
    """
    Return a file path

    The file is one that exists in the repo
    returned by http_repo_url() and ssh_repo_url()

    Remove the file if it exists on teardown
    """
    ret = 'Cargo.toml'
    yield ret

    loc_path = Path(ret)
    if loc_path.exists() and loc_path.is_file():
        loc_path.unlink()


@pytest.fixture
def path_dir_str() -> Generator[str, Any, None]:
    """
    Return a directory path

    The directory is one that exists in the repo
    returned by http_repo_url() and ssh_repo_url()

    Remove the directory if it exists on teardown
    """
    ret = 'xtask'
    yield ret

    loc_path = Path(ret)
    if loc_path.exists() and loc_path.is_dir():
        rmtree(loc_path)


@pytest.fixture(scope='session')
def dir_content() -> Generator[Path, Any, None]:
    """
    Return a list of path object

    The list is a representation of the content of the directory returned by 'path_dir()'
    """
    paths = {
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
    }

    yield paths


@pytest.fixture
def http_repo_url() -> Generator[str, Any, None]:
    """
    Return a github repo's HTTP URL
    """
    yield 'https://github.com/zellij-org/zellij'


@pytest.fixture
def ssh_repo_url() -> Generator[str, Any, None]:
    """
    Return a github repo's SSH URL
    """
    yield 'git@github.com:zellij-org/zellij.git'


@pytest.fixture
def reference_tag() -> Generator[str, Any, None]:
    """
    Reference tag fixture

    Return a tag that exists in the repo returned
    by http_repo_url() and ssh_repo_url()
    """
    yield 'v0.42.2'


@pytest.fixture
def reference_sha() -> Generator[str, Any, None]:
    """
    Reference SHA fixture

    Return a SHA that exists in the repo returned
    by http_repo_url() and ssh_repo_url()
    """
    yield 'a1693ab2a867b8b383a0354d3d6c74e4b76950b0'


# ------------------------------------------------------------------------------


def test_download_file_http(path_file_str, http_repo_url) -> None:
    githubdl.dl_file(
        repo_url=http_repo_url,
        file_name=path_file_str,
    )

    path_obj = Path(path_file_str)
    assert path_obj.is_file()
    assert path_obj.stat().st_size > 0


def test_download_file_http_by_sha_reference_file_present(
    path_file_str,
    http_repo_url,
    reference_sha,
) -> None:
    githubdl.dl_file(
        repo_url=http_repo_url,
        file_name=path_file_str,
        reference=reference_sha,
    )

    path_obj = Path(path_file_str)
    assert path_obj.is_file()
    assert path_obj.stat().st_size > 0


def test_download_file_http_by_tag_reference_file_present(
    path_file_str,
    http_repo_url,
    reference_tag,
) -> None:
    githubdl.dl_file(
        repo_url=http_repo_url,
        file_name=path_file_str,
        reference=reference_tag,
    )

    path_obj = Path(path_file_str)
    assert path_obj.is_file()
    assert path_obj.stat().st_size > 0


def test_download_directory_http(path_dir_str, http_repo_url, dir_content) -> None:
    githubdl.dl_dir(
        repo_url=http_repo_url,
        base_path=path_dir_str,
    )

    path_obj = Path(path_dir_str)
    assert path_obj.is_dir()

    for x in dir_content['dirs']:
        x_path = Path(x)
        assert x_path.exists()
        assert x_path.is_dir()

    for x in dir_content['files']:
        x_path = Path(x)
        assert x_path.exists()
        assert x_path.is_file()


def test_download_file_ssh(path_file_str, ssh_repo_url) -> None:
    githubdl.dl_file(
        repo_url=ssh_repo_url,
        file_name=path_file_str,
    )

    path_obj = Path(path_file_str)
    assert path_obj.is_file()
    assert path_obj.stat().st_size > 0


def test_download_directory_ssh(path_dir_str, ssh_repo_url, dir_content) -> None:
    githubdl.dl_dir(
        repo_url=ssh_repo_url,
        base_path=path_dir_str,
    )

    path_obj = Path(path_dir_str)
    assert path_obj.is_dir()

    for x in dir_content['dirs']:
        x_path = Path(x)
        assert x_path.exists()
        assert x_path.is_dir()

    for x in dir_content['files']:
        x_path = Path(x)
        assert x_path.exists()
        assert x_path.is_file()
