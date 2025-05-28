"""
Pytest fixtures
"""

from pathlib import Path

import pytest
from dotenv import load_dotenv

# ruff: noqa: ANN001


@pytest.fixture(scope='session', autouse=True)
def load_env_from_dotenv() -> None:
    """
    Load environment variables from .env file
    """
    load_dotenv()


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
