"""
URLs processing module
"""

from logging import getLogger
from re import match as re_match
from urllib.parse import urlparse

_logger = getLogger('githubdl')


def generate_repo_api_url(
    repo_url: str,
    file_name: str | None,
    reference: str | None,
    api_path: str,
) -> str:
    """
    Generate the HTTP repo URL that will be used to query the Github API
    """
    url_type, domain_name, repo_name = get_url_components(repo_url)

    if url_type is None:
        err_message = 'Error: repository url provided is not http(s) or ssh'
        _logger.critical(err_message)
        raise RuntimeError(err_message)

    return generate_github_api_url(
        repo_name=repo_name,
        domain_name=domain_name,
        file_name=file_name,
        reference=reference,
        api_path=api_path,
    )


def get_url_components(repo_url: str) -> tuple[str | None, str | None, str | None]:
    """
    Extract the URL type, domain name and the repo name from an SSH or an HTTP URL
    """
    # SSH repo URL
    if (res := re_match(r'git@(.+?):(.+?)\.git$', repo_url)) is not None:
        return (
            'ssh',
            res.group(1),
            res.group(2),
        )

    # HTTP repo URL
    if re_match(r'https?://.*$', repo_url) is not None:
        return (
            'http',
            urlparse(repo_url).netloc,
            urlparse(repo_url).path.removesuffix('.git').removeprefix('/'),
        )

    return None, None, None


def generate_request_string(file_name: str | None, reference: str | None) -> str:
    """
    Generate the last part of the URL for the request
    """
    reference = '' if reference is None else f'?ref={reference}'

    if file_name is not None or reference:
        return f'/{file_name}{reference}'

    return ''


def generate_github_api_url(
    repo_name: str,
    domain_name: str,
    file_name: str,
    reference: str | None,
    api_path: str,
) -> str:
    """
    Return the API URL depending on the domain name (Github /Github Enterprise)
    """
    request_string = generate_request_string(file_name, reference)

    _logger.info('repo_name: %s api_path: %s request_string: %s', repo_name, api_path, request_string)

    if domain_name.lower() == 'github.com':
        return f'https://api.github.com/repos/{repo_name}/{api_path}{request_string}'

    return f'https://{domain_name}/api/v3/repos/{repo_name}/{api_path}{request_string}'
