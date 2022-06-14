# Change Log

All notable changes to this project will be documented in this file.

## [1.6.2] - 2022-06-14

### Added / Changed

- Updated to dash 2.5.1 in requirements
- Updated multipage template

## [1.6.1] - 2022-06-12

### Added / Changed

- Verify generated heroku app name on deploy. This fixes bug where generated name is too long or invalid.

## [1.6.0] - 2022-06-05

### Added / Changed

- Generate Procfile programatically based on location of `app,py` file. This allows users to upload any app to Heroku without needing a Procfile, requirements or runtime file.
- Added retry for random heroku name generation
- Added verify pip command workds on user system after init
- Updated README

## [1.5.1] - 2022-05-29

### Changed

- Added utf8 encoding to verify_procfile method

## [1.5] - 2022-05-29

### Added / Changed

- Added `packages.txt` file to template root directory. Specify required packages on each new line, like a requirements.txt file, and user will be prompted to install if it is not found when they do `dashtools init <template>`
- Cleaned up Docs directory and README (huge thanks to https://github.com/Coding-with-Adam)
- Fixed `run` command to try different python shell commands
- Added config file to store python shell settings
- Added `run --set-python-shell-cmd` to set the python shell command in config
- General prompting hint fixes and updates

### Templates

- Added leaflet template [Dash Leaflet](https://github.com/thedirtyfew/dash-leaflet)

## [1.4] - 2022-05-22

**dash-tools command is now dashtools via command line**

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
- Updated help cli print message, try: `dashtools`

### Templates

- Added fast-dash template https://fastdash.app/
- Added dash-iconify template https://github.com/snehilvj/dash-iconify
