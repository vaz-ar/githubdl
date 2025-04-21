"""
API tests
"""

# ruff: noqa: S101

import os
import shutil
from pathlib import Path

import githubdl


class TestApi:
    """
    API tests class
    """

    @classmethod
    def setup_class(cls) -> None:
        cls.single_file_name = 'README.md'
        cls.single_dir_name = 'support'
        cls.test_repo_url_http = 'https://github.com/wilvk/pbec'
        cls.test_repo_url_ssh = 'git@github.com:wilvk/pbec.git'

    def teardown(self) -> None:
        self.cleanup()

    def setup(self) -> None:
        self.cleanup()

    def is_single_file_present(self):
        single_file = Path(self.single_file_name)
        return single_file.is_file()

    def is_single_file_nonzero(self):
        file_info = os.stat(self.single_file_name)
        return file_info.st_size > 0

    def is_single_dir_present(self):
        single_dir = Path(self.single_dir_name)
        return single_dir.is_dir()

    def cleanup(self) -> None:
        if self.is_single_file_present():
            os.remove(self.single_file_name)
        if self.is_single_dir_present():
            shutil.rmtree(self.single_dir_name)

    def test_can_download_file_http_fille_present(self) -> None:
        githubdl.dl_file(self.test_repo_url_http, self.single_file_name)
        assert self.is_single_file_present()

    def test_can_download_file_http_file_size_non_zero(self) -> None:
        githubdl.dl_file(self.test_repo_url_http, self.single_file_name)
        assert self.is_single_file_nonzero()

    def test_can_download_file_http_by_sha_reference_file_present(self) -> None:
        githubdl.dl_file(self.test_repo_url_http, self.single_file_name, reference='bfef53')
        assert self.is_single_file_present()

    def test_can_download_file_http_by_tag_reference_file_present(self) -> None:
        githubdl.dl_file(self.test_repo_url_http, self.single_file_name, reference='read_working')
        assert self.is_single_file_present()

    def test_can_download_file_http_by_sha_reference_file_size_non_zero(self) -> None:
        githubdl.dl_file(self.test_repo_url_http, self.single_file_name, reference='bfef53')
        assert self.is_single_file_nonzero()

    def test_can_download_file_http_by_tag_reference_file_size_non_zero(self) -> None:
        githubdl.dl_file(self.test_repo_url_http, self.single_file_name, reference='read_working')
        assert self.is_single_file_nonzero()

    def test_can_download_single_directory_http(self) -> None:
        githubdl.dl_dir(self.test_repo_url_http, self.single_dir_name)
        assert self.is_single_dir_present()

    def test_can_download_file_ssh(self) -> None:
        githubdl.dl_file(self.test_repo_url_ssh, self.single_file_name)
        assert self.is_single_file_present()

    def test_can_download_single_directory_ssh(self) -> None:
        githubdl.dl_dir(self.test_repo_url_ssh, self.single_dir_name)
        assert self.is_single_dir_present()
