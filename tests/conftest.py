"""
Pytest fixtures
"""

from collections.abc import Generator
from pathlib import Path
from shutil import rmtree
from typing import Any

import pytest


# ruff: noqa: ANN001
# ruff: noqa: D401


@pytest.fixture(autouse=True)
def change_test_dir(monkeypatch) -> None:
    """
    Change the working directory before running the tests

    Also create the directory if it does not exists
    """
    localpath = Path('tests_data')
    if not localpath.exists():
        localpath.mkdir(parents=True)
    monkeypatch.chdir(localpath)


@pytest.fixture
def path_single_file() -> Generator[Path, Any, None]:
    """
    Return a single file path object

    The file is one that exists in the repo
    returned by http_repo_url() and ssh_repo_url()

    Remove the file if it exists on teardown
    """
    ret = Path('README.md')
    yield ret

    if ret.exists() and ret.is_file():
        ret.unlink()


@pytest.fixture
def path_dir() -> Generator[Path, Any, None]:
    """
    Return a directory path object

    The directory is one that exists in the repo
    returned by http_repo_url() and ssh_repo_url()

    Remove the directory if it exists on teardown
    """
    ret = Path('xtask')
    yield ret

    if ret.exists() and ret.is_dir():
        rmtree(ret)


@pytest.fixture()
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
