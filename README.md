
# Github Path Downloader

A tool for downloading individual files/directories from Github or Github Enterprise.

This circumvents the requirement to clone a complete repository.

## Requirements

- Python 3.10+
- A Github or Github Enterprise Account

## Install

~~~bash
uv tool install --from=https://github.com/vaz-ar/githubdl.git githubdl
~~~

## Usage

### Obtaining a Github token

You will need a token from either Github Enterprise or Github as this package works with the Github v3 API.

There are instructions on how to do this [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).


## Command line usage

With your Github token, export it as the environment variable `GITHUB_TOKEN`.

### On Unix/Linux

~~~bash
$ export GITHUB_TOKEN=1234567890123456789012345678901234567890123
~~~

### Single file

Then, for example, to download a file called `README.md` from the repository `http://github.com/wilvk/pbec`:

~~~bash
$ githubdl -u "http://github.com/wilvk/pbec" -f "README.md"
2018-05-12 07:19:16,934 - root         - INFO     - Requesting file: README.md at url: https://api.github.com/repos/wilvk/pbec/contents/README.md
2018-05-12 07:19:18,165 - root         - INFO     - Writing to file: README.md
~~~

### Entire directory

~~~bash
$ githubdl -u "http://github.com/wilvk/pbec" -d "support"
2018-05-12 07:19:41,667 - root         - INFO     - Retrieving a list of files for directory: support
2018-05-12 07:19:41,668 - root         - INFO     - Requesting file: support at url: https://api.github.com/repos/wilvk/pbec/contents/support
2018-05-12 07:19:42,978 - root         - INFO     - Requesting file: support/Screen Shot 2017-12-10 at 9.27.56 pm.png at url: https://api.github.com/repos/wilvk/pbec/contents/support/Screen Shot 2017-12-10 at 9.27.56 pm.png
2018-05-12 07:19:46,274 - root         - INFO     - Writing to file: support/Screen Shot 2017-12-10 at 9.27.56 pm.png
2018-05-12 07:19:46,286 - root         - INFO     - Retrieving a list of files for directory: support/docker
~~~

### Entire repository

~~~bash
$ githubdl -u "http://github.com/wilvk/pbec" -d "/" -t "."
~~~

Note: if `-t` is not set, output will go to your `/` directory.

### By commit hash

### Single file from a specific commit

~~~bash
$ githubdl -u "http://github.com/wilvk/pbec" -f "README.md" -r "c29eb5a5d364870a55c0c22f203f8c4e2ce1c638"
~~~

### Entire directory from a specific commit

~~~bash
$ githubdl -u "http://github.com/wilvk/pbec" -d "support" -r "c29eb5a5d364870a55c0c22f203f8c4e2ce1c638"
~~~

### Entire repository from a specific commit

~~~bash
$ githubdl -u "http://github.com/wilvk/pbec" -d "/" -r "c29eb5a5d364870a55c0c22f203f8c4e2ce1c638" -t "."
~~~

Note: if `-t` is not set, output will go to your `/` directory.

### Entire repository from a specific commit, with submodules (as specified in .gitmodules)

~~~bash
$ githubdl -u "http://github.com/wilvk/pbec" -d "/" -r "c29eb5a5d364870a55c0c22f203f8c4e2ce1c638" -t "." -s
~~~

### List all tags for a repository in JSON

~~~bash
$ githubdl -u "http://github.com/wilvk/pbec" -a
~~~

### List all branches for a repository in JSON

~~~bash
$ githubdl -u "http://github.com/wilvk/pbec" -b
~~~


## Logging

Valid log levels are: `DEBUG`, `INFO`, `WARN`, `ERROR`, `CRITICAL`

## References

References can be applied to file and directory download only and consist of valid:

  - repository tags
  - commit SHAs
  - branch names.
