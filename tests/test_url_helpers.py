#!/usr/local/bin/python

import inspect
import os
import sys

import url_helpers as uh

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
includedir = os.path.join(parentdir, 'githubdl')
sys.path.insert(0, includedir)


class TestUrlHelpers:
    def test_check_url_is_http_http(self) -> None:
        result = uh.check_url_is_http('http://test.com')
        assert result

    def test_check_url_is_http_https(self) -> None:
        result = uh.check_url_is_http('https://test.com')
        assert result

    def test_check_url_is_not_http_1(self) -> None:
        result = uh.check_url_is_http('httpxx://test.com')
        assert not result

    def test_check_url_is_not_http_2(self) -> None:
        result = uh.check_url_is_http('htp://test.com')
        assert not result

    def test_check_url_is_ssh(self) -> None:
        result = uh.check_url_is_ssh('git@github.com:pypa/sampleproject.git')
        assert result

    def test_check_url_is_not_ssh_invalid_user(self) -> None:
        result = uh.check_url_is_ssh('giti_@github.com:pypa/sampleproject.git')
        assert not result

    def test_check_url_is_not_ssh_slash(self) -> None:
        result = uh.check_url_is_ssh('git@test.com/test.git')
        assert result

    def test_check_url_is_not_ssh_http(self) -> None:
        result = uh.check_url_is_ssh('htp://test.com')
        assert not result

    def test_get_domain_name_from_http(self) -> None:
        result = uh.get_domain_name_from_http_url('https://github.com/pypa/sampleproject.git')
        assert result == 'github.com'

    def test_get_repo_name_from_http_url(self) -> None:
        result = uh.get_repo_name_from_http_url('https://github.com/pypa/sampleproject.git')
        assert result == 'pypa/sampleproject'

    def test_get_domain_name_from_ssh_url(self) -> None:
        result = uh.get_domain_name_from_ssh_url('git@github.com:pypa/sampleproject.git')
        assert result == 'github.com'

    def test_get_repo_name_from_ssh_url(self) -> None:
        result = uh.get_repo_name_from_ssh_url('git@github.com:pypa/sampleproject.git')
        assert result == 'pypa/sampleproject'
