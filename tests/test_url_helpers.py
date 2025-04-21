"""
URLs helpers tests
"""

# ruff: noqa: S101

from githubdl import url_helpers as uh


def test_check_url_is_http_http() -> None:
    assert uh.check_url_is_http('http://test.com')


def test_check_url_is_http_https() -> None:
    assert uh.check_url_is_http('https://test.com')


def test_check_url_is_not_http_1() -> None:
    assert not uh.check_url_is_http('httpxx://test.com')


def test_check_url_is_not_http_2() -> None:
    assert not uh.check_url_is_http('htp://test.com')


def test_check_url_is_ssh() -> None:
    assert uh.check_url_is_ssh('git@github.com:pypa/sampleproject.git')


def test_check_url_is_not_ssh_invalid_user() -> None:
    assert not uh.check_url_is_ssh('giti_@github.com:pypa/sampleproject.git')


def test_check_url_is_not_ssh_slash() -> None:
    assert uh.check_url_is_ssh('git@test.com/test.git')


def test_check_url_is_not_ssh_http() -> None:
    assert not uh.check_url_is_ssh('htp://test.com')


def test_get_domain_name_from_http() -> None:
    result = uh.get_domain_name_from_http_url('https://github.com/pypa/sampleproject.git')
    assert result == 'github.com'


def test_get_repo_name_from_http_url() -> None:
    result = uh.get_repo_name_from_http_url('https://github.com/pypa/sampleproject.git')
    assert result == 'pypa/sampleproject'


def test_get_domain_name_from_ssh_url() -> None:
    result = uh.get_domain_name_from_ssh_url('git@github.com:pypa/sampleproject.git')
    assert result == 'github.com'


def test_get_repo_name_from_ssh_url() -> None:
    result = uh.get_repo_name_from_ssh_url('git@github.com:pypa/sampleproject.git')
    assert result == 'pypa/sampleproject'
