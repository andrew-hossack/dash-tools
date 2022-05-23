# Change Log

All notable changes to this project will be documented in this file.

## [1.4] - 2022-05-22

Major changes are an overhaul to the CLI entry to use subcommands. This looks like a change from this: `dash-tools --init MyApp tabs` to `dash-tools init MyApp tabs`. Also added a few new commands.

### Added / Changed

- Added subparsers to CLI to make commands look better:
  - `dash-tools init <app name> [<template>]`
- Added `-d` or `--dir` for `init` to specify create directory
- Added new `--update` command to directly update to "heroku" remote
  - `dash-tools heroku --update`
- Broke out heroku deploy command
  - `dash-tools heroku --deploy`
- Broke out templates commands to use list, and added a new command to change specified directory into a new template directory. When running this command, `--init` will copy the specified directory to current directory with the name `Template` appended. All files will be given `.template` extensions.
  - `dash-tools templates --list`
  - `dash-tools templates --init <directory to copy>`
- Added `dash-tools run` command to run the app.py file (recursive search for app.py file, if not specified in a Procfile)

### Templates

- Added fast-dash template https://fastdash.app/
- Added dash-iconify template https://github.com/snehilvj/dash-iconify

### Fixed
