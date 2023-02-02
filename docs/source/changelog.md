# Changelog

All notable changes to this project will be documented in this file.

## [1.11.0] - 2023-2-01

### Added & Changed

- Added create page, and the ability to explore between different template previews
- Create templated apps using the `dashtools gui`
- Lots of style changes
- Added links to bottom of screen
- Added github star link
- Fixed some issues with os path not being normalized
- Added `--no-update-check` flag to `dashtools init` to skip PyPi version checking
- Silenced output for gui
- Removed gui threading, seems like this is no longer needed since the start script is fixed (does not run twice)

## [1.10.8] - 2023-1-29

### Added

- Added github star link

## [1.10.7] - 2022-12-24

### Modified

- Upgraded PYTHON_VERSION to 3.10.0 for Render blueprint
- Snyk upgrade for setuptools vulnerability

## [1.10.6] - 2022-12-16

### Modified

- Updated naming on github workflows
- Added a create tag and release action on push to main. Takes current version and latest stuff from the changelog in the release notes.

## [1.10.5] - 2022-12-16

### Fixed

- Fixed background callbacks printing warnings on new version of plotly dash
- Update pypa publish to use v1 release
- Fixed issue with deploypage callbacks not working in some cases
- Update gitlab runner to python version 3.10.9

## [1.10.4] - 2022-11-8

### Fixed

- Fixed bug with background callback requiring cellery worker or diskcache, due to Dash 2.7.0 upgrade
- Fixed read the docs templates list accordions not displaying
- Changed dockerfile to use non root user; credit [@jasonwashburn](https://github.com/jasonwashburn)
- Fixed CI/CD build process to install dashtools tar file; credit [@jasonwashburn](https://github.com/jasonwashburn)

## [1.10.3] - 2022-10-30

### Fixed

- Fixed bug with running os commands on windows; thanks [@Coding-with-Adam](https://github.com/Coding-with-Adam) for support!

## [1.10.2] - 2022-10-26

### Fixed

- Fixed bug https://github.com/andrew-hossack/dash-tools/issues/65 where using http for git remote url doesn't work; thanks [@mtzirkel](https://github.com/mtzirkel) for support!

## [1.10.1] - 2022-10-23

### Changed

- Turn off logging and debug mode for gui server
- Address bug where server opens twice
- Open web url in browser when server starts
- Updated packaging structure to exclude 'docs' module which should not have been there
- Temporarily disabled tests for this release. Test suite needs to be overhauled for current changes.

## [1.9.2] - 2022-10-18

### Fixed

- Made published to github a project requirement instead of an error

## [1.9.1] - 2022-10-17

### Fixed

- Added missing dependency

## [1.9.0] - 2022-10-17

### Added

- Added `dashtools gui` render deploy dashboard

## [1.8.4] - 2022-9-09

### Fixed

- Updated heroku default runtime to 3.10.7

## [1.8.3] - 2022-08-29

### Fixed

- Changed heroku app name verification again. Heroku sends back a 404 if no app name is in use. Thanks @lanchuhuong!

## [1.8.2] - 2022-08-12

### Fixed

- Pipreqs generating requirements.txt does not work on some systems. Fixed with calling pipreqs.init(args) directly.

## [1.8.1] - 2022-08-12

### Changed

- Print out error message for pipreqs errors

## [1.8.0] - 2022-08-10

### Added

- Added pypi version check to prompt user if their current version is out of date

## [1.7.3] - 2022-08-09

### Fixed

- Fixed bug with Heroku HTTP request. When validating heroku name availability, a request is sent to heroku. Their server changed from a 404 response to an "This site can’t be reached" response. Fixed method for validating heroku app name.

## [1.7.2] - 2022-07-28

### Changed

- Renamed `run --set-py-cmd` command

## [1.7.1] - 2022-07-21

### Changed

- Fixed `advanced` template issues where it will not run.

## [1.7.0] - 2022-06-27

### Added

- Added `docker --init` command; creates a docker image in the current directory. Adds requirements.txt file and Dockerfile in the current directory if one isn't found.

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

- **dash-tools command is now dashtools via command line**
- Major changes are an overhaul to the CLI entry to use subcommands. This looks like a change from this: `dashtools --init MyApp tabs` to `dashtools init MyApp tabs`. Also added a few new commands.

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
