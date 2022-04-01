# dash-tools - An Open-Source Plotly Dash CLI Toolchain

Create a Plotly Dash app with CLI.

[Plotly Dash](https://plotly.com/dash/)

## Installation

`dash-tools` is available through pip.

```bash
pip install dash-tools
```

## Commands

### Project Templating

- **`--init, -i` Args: (`project name`) :** Creates a Plotly Dash app with the given name in the current working directory.
- **`--use_stack` Args: (`heroku`) :** Add stack to current project. Currently only supports Heroku.

### Debug and Run

- **`--run, -r`:** Run the current project in non-debug mode.
- **`--dev, -d`:** Run the current project in debug/dev mode.

## Development

### Creating Templates

Templates go in the `dash_tools/templating/templates` directory, and follow the naming convention `<name>.<extension>.template`

When installed through `buildTemplate:create_app`, templates are written to the user's file system after being run through a formatter.

Formatting in templates is simple. In `fileUtils:format_file_stream`, placeholders such as `{appName}` can be replaces with variables during runtime.
