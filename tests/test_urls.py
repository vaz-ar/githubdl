"""
URLs related tests
"""

# ruff: noqa: S101

from githubdl import url_processing as up


def test_url_http_domain() -> None:
    data = up.get_url_components('http://test.com')
    assert data is not None
    assert data[0] == 'http'
    assert data[1] == 'test.com'
    assert data[2] is not None


def test_url_https_domain() -> None:
    data = up.get_url_components('https://test.com')
    assert data is not None
    assert data[0] == 'http'
    assert data[1] == 'test.com'
    assert data[2] is not None


def test_url_not_http_1() -> None:
    data = up.get_url_components('httpxx://test.com')
    assert data is not None
    for i in range(3):
        assert data[i] is None


def test_url_not_http_2() -> None:
    data = up.get_url_components('htp://test.com')
    assert data is not None
    for i in range(3):
        assert data[i] is None


def test_git_url_ssh() -> None:
    data = up.get_url_components('git@github.com:pypa/sampleproject.git')
    assert data is not None
    assert data[0] == 'ssh'
    assert data[1] == 'github.com'
    assert data[2] == 'pypa/sampleproject'


def test_url_ssh_invalid_user() -> None:
    data = up.get_url_components('giti_@github.com:pypa/sampleproject.git')
    assert data is not None
    for i in range(3):
        assert data[i] is None


def test_url_ssh_slash() -> None:
    data = up.get_url_components('git@test.com/test.git')
    assert data is not None
    for i in range(3):
        assert data[i] is None


def test_git_url_https() -> None:
    data = up.get_url_components('https://github.com/pypa/sampleproject.git')
    assert data is not None
    assert data[0] == 'http'
    assert data[1] == 'github.com'
    assert data[2] == 'pypa/sampleproject'
