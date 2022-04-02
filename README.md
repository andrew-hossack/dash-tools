# dash-tools - An Open-Source Plotly Dash CLI Toolchain

Create a Plotly Dash app with CLI.

[Plotly Dash](https://plotly.com/dash/)

## Installation

`dash-tools` is available through pip.

```bash
pip install dash-tools
```

## Examples

Below are common usage examples. See _Commands_ section for more details.

```bash
# Create a new Dash app called MyDashApp
dash-tools --init MyDashApp
```

Templates are also available using the optional template argument after --init:

```bash
# Create a new Dash app called MyDashApp using 'minimal' theme
dash-tools --init MyDashApp minimal
```

## Commands

### Project Build Commands

- **`--init, -i` Args: REQUIRED (`project name`) OPTIONAL (`template`) :** Creates a Plotly Dash app with the given name in the current working directory. Optional args specified can be used for templates. Available templates available are `default` and `minimal`.
- **`--use_stack` Args: (`heroku`) :** Add stack to current project. Currently only supports Heroku.

### Debug and Run

- **`--run, -r`:** Run the current project in non-debug mode.
- **`--dev, -d`:** Run the current project in debug/dev mode.

## Development

### Creating Templates

Templates go in the `dash_tools/templating/templates` directory. The entire directory structure will be copied to the users source directory if they choose the correct Templates Enum.

Adding a new template to the templates directory also requires adding the new template to the Enum list in `buildTemplate:Templates` Enum. Template name must match Enum value!

Any file name or file containing the strings `{appName}` or `{createTime}` will be formatted with the given app name and creation time.
