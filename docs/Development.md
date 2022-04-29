# 🛠️ **dash-tools** - _Developer Guide_

Thank you for showing interest in dash-tools. When I created the project, I wanted to build the solution for Plotly Dash project templates and easy deployment.

If you are interested in supporting this project, feel free to [Create a PR](https://github.com/andrew-hossack/dash-tools/pulls), [Submit an Issue](https://github.com/andrew-hossack/dash-tools/issues), or reach out to me at my email [andrewhossack@live.com](mailto:andrewhossack@live.com). Thanks!

## **Creating Templates**

1. Templates are found here: `dash_tools/templating/templates/<Template Name>`. When a user uses CLI to choose a template with the name `<Template Name>` the template will be copied to their system.
2. Adding a new template to the templates directory requires adding the new template to the Enum list in `templating.Templates` Enum. Template name must match Enum value, eg.

   ```python
   class Templates(Enum):
      DEFAULT = 'default'
      MINIMAL = 'minimal'
      NEWTEMPLATE = 'newtemplate'
   ```

3. Any file names or files containing the strings `{appName}` or `{createTime}` will be formatted with the given app name and creation time. Eg. _README.md.template_: `# Created on {createTime}` will copy to the user's filesystem as _README.md_: `# Created on 2022-03-30 22:06:07`
4. All template files must end in `.template`

## **Testing**

Run pre-commit:

```bash
pre-commit install
```
