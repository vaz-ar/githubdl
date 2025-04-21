"""
Githubdl main module
"""

import argparse
import logging
from json import dump as json_dump
from json import loads as json_loads
from os import environ
from pathlib import Path

from .api import dl_branches, dl_dir, dl_file, dl_tags

_logger = logging.getLogger('githubdl')


def set_github_token(github_token: str) -> None:
    """
    Set the github token at env level

    If not github token was passed as parameter and
    GITHUB_TOKEN is not set in the environment an exception will be raised
    """
    if not environ.get('GITHUB_TOKEN'):
        if not github_token:
            err_message = (
                "Unable to find Github token either as a parameter or the in environment variable 'GITHUB_TOKEN'"
            )
            _logger.critical(err_message)
            raise RuntimeError(err_message)

        environ['GITHUB_TOKEN'] = github_token


def set_log_level(args: dict[str, str]) -> int:
    """
    Set the log level based on the log_level arg
    """
    if (level := args.get('log_level')) is not None:
        match level:
            case 'DEBUG':
                return logging.DEBUG
            case 'INFO':
                return logging.INFO
            case 'WARN':
                return logging.WARNING
            case 'ERROR':
                return logging.ERROR
            case 'CRITICAL':
                return logging.CRITICAL
            case _:
                return logging.INFO

    if args['tags'] or args['branches']:
        return logging.WARNING

    return logging.INFO


def main() -> None:
    """
    Main entrypoint for the cli application
    """
    parser = argparse.ArgumentParser(
        description=(
            'Github Path Downloader. '
            'Download files and directories from Github easily. '
            'Works with Github and Github Enterprise.'
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        '-f',
        '--file',
        help='The name of the file to download.',
        required=False,
    )
    group.add_argument(
        '-d',
        '--dir',
        help='The name of the directory to download.',
        required=False,
    )
    group.add_argument(
        '-a',
        '--tags',
        help='A switch specifying that a list of tags is to be downloaded.',
        required=False,
        action='store_true',
    )
    group.add_argument(
        '-b',
        '--branches',
        help='A switch specifying that a list of branches is to be downloaded.',
        required=False,
        action='store_true',
    )

    parser.add_argument('-u', '--url', help='The url of the repository to download.', required=True)
    parser.add_argument(
        '-t',
        '--target',
        help='The name of the file or directory to save the data to. Defaults to file or directory name.',
        required=False,
    )
    parser.add_argument(
        '-g',
        '--git_token',
        help='The value of the Github/Github Enterprise Token. Can also be specified in the environment variable GITHUB_TOKEN.',
        required=False,
    )
    parser.add_argument(
        '-l',
        '--log_level',
        help='The level of logging to use for output. Valid options are: DEBUG, INFO, WARN, ERROR, CRITICAL. Defaults to INFO.',
        required=False,
    )
    parser.add_argument(
        '-r',
        '--reference',
        help="The name of the commit/branch/tag. Default: the repository's default branch.",
        required=False,
    )
    parser.add_argument(
        '-s',
        '--submodules',
        help='A switch specifying that all submodules are to be downloaded.',
        required=False,
        # store_true automatically sets the default value to False
        action='store_true',
    )

    args = vars(parser.parse_args())

    logging.basicConfig(
        level=set_log_level(args),
        format='%(asctime)s  %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    set_github_token(args.get('github_token'))

    target = ''
    reference = ''

    if args['target'] is not None:
        target = args['target']

    if args['reference'] is not None:
        reference = args['reference']

    # --------------------------------------------------------------------------

    if args['tags']:
        with Path('tags.json').open(mode='w', encoding='utf-8') as f:
            _logger.info('Writing tags list as branches.json')
            json_dump(json_loads(dl_tags(args['url'])), f, indent=2)

    elif args['branches']:
        with Path('branches.json').open(mode='w', encoding='utf-8') as f:
            _logger.info('Writing branches list as branches.json')
            json_dump(json_loads(dl_branches(args['url'])), f, indent=2)

    elif args['file'] is not None:
        dl_file(
            repo_url=args['url'],
            file_name=args['file'],
            target_filename=target,
            reference=reference,
        )

    elif args['dir'] is not None:
        dl_dir(
            repo_url=args['url'],
            base_path=args['dir'],
            target_path=target,
            reference=reference,
            submodules=args['submodules'],
        )


if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement.
    main()
