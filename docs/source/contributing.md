# Contributing

## Getting Started

Thank you for showing interest in dash-tools! To set up your environment, run the following commands:

```bash
# in your working directory
$ git clone git@github.com:andrew-hossack/dash-tools.git
$ cd dash-tools
# install the package
$ pip install . --upgrade
# install testing resources
$ pre-commit install
$ pre-commit run --all-files
```

## What to contribute

Found a bug? See something you aren't a fan of? Want to propose an addition? Here are some common contributions and good places to start.

### Templates

1. Templates are found in the `dash_tools/templating/templates/` directory. When a user chooses a template with the name `<Template Name>` the template will be copied to their system. For example, if they run `dash-tools --init MyDashApp default`, the _default_ template will be used, which corresponds with the `dash_tools/templating/templates/default/` directory.
2. Adding a new template to the templates directory requires adding the new template to the Enum list in `templating.Templates.py` `Template` Enum. The Template directory name must match Enum value, eg. 'DEFAULT' template uses the `/default` template directory.

   ```python
   class Templates(Enum):
      DEFAULT = 'default'
      MINIMAL = 'minimal'
      NEWTEMPLATE = 'newtemplate'
   ```

3. Any file names or files containing the strings `{appName}` or `{createTime}` will be formatted with the given app name and creation time. Eg. _README.md.template_: `# Created on {createTime}` will copy to the user's filesystem as _README.md_: `# Created on 2022-03-30 22:06:07`
4. All template files must end in `.template`

### Write Tests

Pytest is used for testing (see [Tests](#tests)). Unittests are needed to verify code works as intended. Unittests would be a great place to start, as they will make you familiar with the repo and are needed to promote code quality.

### Add to Common Errors and Troubleshooting Section

Common errors and troubleshooting README section should be the first place dash-tools users look when they encounter an error. By contributing to this readme section, you are helping ease the pain of problem solving.

## Tests

[Pytest](https://docs.pytest.org/en/latest/) is used for testing. Most of the time, you will want to just run a few relevant tests and let GitHub actions run the whole suite. `pytest` lets you specify a directory or file to run tests from (eg `pytest tests/unit`).

### Unit Tests

For simple API changes, please add adequate unit tests under `/tests`

## Financial Contributions

This project is sponsored by helpful people like you! Please feel free to reach out directly to andrew_hossack@outlook.com or [Donate](https://github.com/sponsors/andrew-hossack) if you would like to help out this project. Thanks!
