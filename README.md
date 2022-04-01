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
