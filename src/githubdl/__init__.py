"""
Githubdl main module
"""

import argparse
import logging
from json import dump as json_dump
from os import environ
from pathlib import Path
from sys import exit as sys_exit

from colorlog import ColoredFormatter, StreamHandler, getLogger
from dotenv import load_dotenv

from .api import dl_branches, dl_dir, dl_file, dl_tags

_logger = getLogger('githubdl')


def set_github_token(github_token: str) -> bool:
    """
    Set the github token at env level

    If not github token was passed as parameter and
    GITHUB_TOKEN is not set in the environment an exception will be raised
    """
    if not environ.get('GITHUB_TOKEN', ''):
        if not github_token:
            _logger.critical(
                "No Github token found, either as a parameter or in the environment variable 'GITHUB_TOKEN'"
            )
            return False

        environ['GITHUB_TOKEN'] = github_token

    return True


def set_log_level(args: dict[str, str]) -> int:
    """
    Set the log level based on the log_level arg
    """
    log_level = logging.INFO

    if (level := args.get('log_level')) is not None:
        match level:
            case 'DEBUG':
                log_level = logging.DEBUG
            case 'INFO':
                log_level = logging.INFO
            case 'WARN':
                log_level = logging.WARNING
            case 'ERROR':
                log_level = logging.ERROR
            case 'CRITICAL':
                log_level = logging.CRITICAL

    if args['tags'] or args['branches']:
        log_level = logging.WARNING

    return log_level


def main() -> None:
    """
    Main entrypoint for the cli application
    """
    load_dotenv(encoding='utf-8')

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
        # store_true automatically sets the default value to False
        action='store_true',
    )
    group.add_argument(
        '-b',
        '--branches',
        help='A switch specifying that a list of branches is to be downloaded.',
        required=False,
        # store_true automatically sets the default value to False
        action='store_true',
    )

    parser.add_argument(
        '-u',
        '--url',
        help='The url of the repository to download.',
        required=True,
    )
    parser.add_argument(
        '-t',
        '--target',
        help='The name of the file or directory to save the data to. Defaults to file or directory name.',
        required=False,
    )
    parser.add_argument(
        '-g',
        '--git_token',
        help='The value of the Github/Github Enterprise Token.'
        'Can also be specified in the environment variable GITHUB_TOKEN.',
        required=False,
    )
    parser.add_argument(
        '-l',
        '--log_level',
        help='The level of logging to use for output. Valid options are: DEBUG, INFO, WARN, ERROR, CRITICAL. '
        'Defaults to INFO.',
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

    # --- logging
    handler = StreamHandler()
    handler.setFormatter(
        ColoredFormatter(
            fmt='%(log_color)s%(asctime)s  %(levelname)-8s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )
    )
    _logger.addHandler(handler)
    _logger.setLevel(set_log_level(args))
    #  ---

    if not set_github_token(str(args.get('github_token'))):
        sys_exit(1)

    if args['tags']:
        with Path('tags.json').open(mode='w', encoding='utf-8') as f:
            _logger.info('Writing tags list as branches.json')
            json_dump(dl_tags(args['url']), f, indent=2)

    elif args['branches']:
        with Path('branches.json').open(mode='w', encoding='utf-8') as f:
            _logger.info('Writing branches list as branches.json')
            json_dump(dl_branches(args['url']), f, indent=2)

    elif args['file'] is not None:
        dl_file(
            repo_url=args['url'],
            file_name=args['file'],
            target_filename=args['target'],
            reference=args['reference'],
        )

    elif args['dir'] is not None:
        dl_dir(
            repo_url=args['url'],
            base_path=args['dir'],
            target_path=args['target'],
            reference=args['reference'],
            submodules=args['submodules'],
        )


if __name__ == '__main__':
    # Execute when the module is not initialised from an import statement.
    main()
