# Change Log

All notable changes to this project will be documented in this file.

## [1.4] - 2022-05-22

**dashtools is now dashtools on PyPi and via command line**

Major changes are an overhaul to the CLI entry to use subcommands. This looks like a change from this: `dashtools --init MyApp tabs` to `dashtools init MyApp tabs`. Also added a few new commands.

### Added / Changed

- Invoke dashtools now by typing: `dashtools <command>` (was `dash-tools <command>` before)
- Added subparsers to CLI to make commands look better:
  - `dashtools init <app name> [<template>]`
- Added `-d` or `--dir` for `init` to specify create directory, e.g. `dashtools init <appname> [<template>] --dir ~/MySandbox`
- Added new `--update` command to directly update to "heroku" remote
  - `dashtools heroku --update`
- Broke out heroku deploy command
  - `dashtools heroku --deploy`
- Broke out templates commands to use list, and added a new command to change specified directory into a new template directory. When running this command, `--init` will copy the specified directory to current directory with the name `Template` appended. All files will be given `.template` extensions.
  - `dashtools templates --list`
  - `dashtools templates --init <directory to copy>`
- Added `dashtools run` command to run the app.py file (recursive search for app.py file, if not specified in a Procfile)
- Better heroku deployment name generation - takes three random nouns joined by dashes and appends four alphanumeric char to end (ex. mountain-surgeon-chair-h129)
- Added logo

### Templates

- Added fast-dash template https://fastdash.app/
- Added dash-iconify template https://github.com/snehilvj/dash-iconify

### Fixed
