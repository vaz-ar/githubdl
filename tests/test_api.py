"""
API tests
"""

# ruff: noqa: S101
# ruff: noqa: ANN001

from pathlib import Path

import githubdl


def test_download_file_http_file_present(path_single_file, http_repo_url) -> None:
    githubdl.dl_file(
        repo_url=http_repo_url,
        file_name=path_single_file,
    )
    assert path_single_file.is_file()


def test_download_file_http_file_size_non_zero(path_single_file, http_repo_url) -> None:
    githubdl.dl_file(
        repo_url=http_repo_url,
        file_name=path_single_file,
    )
    assert path_single_file.stat().st_size > 0


def test_download_file_http_by_sha_reference_file_present(
    path_single_file,
    http_repo_url,
    reference_sha,
) -> None:
    githubdl.dl_file(
        repo_url=http_repo_url,
        file_name=path_single_file,
        reference=reference_sha,
    )
    assert path_single_file.is_file()


def test_download_file_http_by_tag_reference_file_present(
    path_single_file,
    http_repo_url,
    reference_tag,
) -> None:
    githubdl.dl_file(
        repo_url=http_repo_url,
        file_name=path_single_file,
        reference=reference_tag,
    )
    assert path_single_file.is_file()


def test_download_file_http_by_sha_reference_file_size_non_zero(
    path_single_file,
    http_repo_url,
    reference_sha,
) -> None:
    githubdl.dl_file(
        repo_url=http_repo_url,
        file_name=path_single_file,
        reference=reference_sha,
    )
    assert path_single_file.stat().st_size > 0


def test_download_file_http_by_tag_reference_file_size_non_zero(
    path_single_file,
    http_repo_url,
    reference_tag,
) -> None:
    githubdl.dl_file(
        repo_url=http_repo_url,
        file_name=path_single_file,
        reference=reference_tag,
    )
    assert path_single_file.stat().st_size > 0


def test_download_directory_http(path_dir, http_repo_url) -> None:
    githubdl.dl_dir(
        repo_url=http_repo_url,
        base_path=path_dir,
    )
    assert path_dir.is_dir()


def test_download_file_ssh(path_single_file, ssh_repo_url) -> None:
    githubdl.dl_file(
        repo_url=ssh_repo_url,
        file_name=path_single_file,
    )
    assert path_single_file.is_file()


def test_download_directory_ssh(path_dir, ssh_repo_url, dir_content) -> None:
    githubdl.dl_dir(
        repo_url=ssh_repo_url,
        base_path=path_dir,
    )
    assert path_dir.is_dir()

    for x in dir_content['dirs']:
        x_path = Path(x)
        assert x_path.exists()
        assert x_path.is_dir()

    for x in dir_content['files']:
        x_path = Path(x)
        assert x_path.exists()
        assert x_path.is_file()
