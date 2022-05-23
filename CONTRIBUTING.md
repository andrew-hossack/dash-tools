# Contributor Guide

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

### Add Prompts

Prompts are shown to the user to provide a seamless user experience. If a user encounters a problem, what do they see? By providing useful prompts, dash-tools users will spend less time trying to find the right solution and instead will know what to do.

Prompts are a great place to start contributing.

### Write Tests

Pytest is used for testing (see [Tests](#tests)). Unittests are needed to verify code works as intended. Unittests would be a great place to start, as they will make you familiar with the repo and are needed to promote code quality.

### Add to Common Errors and Troubleshooting Section

Common errors and troubleshooting README section should be the first place dash-tools users look when they encounter an error. By contributing to this readme section, you are helping ease the pain of problem solving.

## Git

Use the [GitHub flow](https://guides.github.com/introduction/flow/) when proposing contributions to this repository (i.e. create a feature branch and submit a PR against the default branch).

### Organize your commits

For pull request with notable file changes or a big feature development, we highly recommend to organize the commits in a logical manner, so it

- Makes a code review experience much more pleasant
- Facilitates a possible cherry picking with granular commits

#### Git Desktop

Git command veterans might argue that a simple terminal and a cherry switch keyboard is the most elegant solution. But in general, a desktop tool makes the task easier:

1. <https://www.gitkraken.com/git-client>
2. <https://desktop.github.com/>

### Emoji

Plotlyers (and dash-tools users) love to use emoji as an effective communication medium for:

**Commit Messages**

Emojis make the commit messages :cherry_blossom:. If you have no idea about what to add ? Here is a nice [cheatsheet](https://gitmoji.carloscuesta.me/) and just be creative!

**Code Review Comments**

- :dancer: `:dancer:` - used to indicate you can merge! Equivalent to GitHub's :squirrel:
- :cow2: `:cow2:` cow tip - minor coding style or code flow point
- :tiger2: `:tiger2:` testing tiger - something needs more tests, or tests need to be improved
- :snake: `:snake:` security snake - known or suspected security flaw
- :goat: `:goat:` grammar goat
- :smile_cat: `:smile_cat:` happy cat - for bits of code that you really like!
- :dolls: `:dolls:` documentation dolls
- :pill: `:pill:` performance enhancing pill
- :hocho: `:hocho:` removal of large chunks of code (obsolete stuff, or feature removals)
- :bug: `:bug:` - a bug of some kind. 8 legged or 6. Sometimes poisonous.
- :camel: :palm_tree: `:camel:` `:palm_tree:` - The Don't Repeat Yourself (DRY) camel or palm tree.
- :space_invader: `:space_invader:` - Too much space or too little.
- :spaghetti: `:spaghetti:` - copy-pasta, used to signal code that was copy-pasted without being updated

### Coding Style

Pre-commit hooks are configured to run [autopep8](https://github.com/pre-commit/mirrors-autopep8). See `.pre-commit-config.yaml` for more information on pre-commit hooks.

## Tests

[Pytest](https://docs.pytest.org/en/latest/) is used for testing. Most of the time, you will want to just run a few relevant tests and let GitHub actions run the whole suite. `pytest` lets you specify a directory or file to run tests from (eg `pytest tests/unit`).

### Unit Tests

For simple API changes, please add adequate unit tests under `/tests`

## TODO List

Other

- create MkDocs-material website https://squidfunk.github.io/mkdocs-material/creating-your-site/
- add a way to upload templates?

## Financial Contributions

This project is sponsored by helpful people like you! Please feel free to reach out directly to andrew_hossack@outlook.com if you would like to support or donate to this project. Thanks!

## Attribution

_Much of this contribution guide is from [Plotly Dash](https://github.com/plotly/dash/blob/dev/CONTRIBUTING.md) - check them out!_
