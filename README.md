# 🛠️ **dash-tools** - _Easily Create and Deploy your Plotly Dash Apps from CLI (V0.10)_

Create a templated multi-page [Plotly Dash](https://plotly.com/dash/) app with CLI in less than 7 seconds.

Deploy your app to [Heroku](https://heroku.com/) in under a minute!

![](docs/intro_gif.gif)

## **About**

[**dash-tools**](https://github.com/andrew-hossack/dash-tools) is an open-source toolchain for [Plotly Dash Framework](https://dash.plotly.com/introduction). With a user-friendly command line interface, creating Dash applications has never been quicker.

Includes user and developer-friendly app templates where generating a new app only takes seconds. In fact, it will take longer to install this tool than it will to use it!

Want to deploy your app to the web? We've got you covered. With [Heroku](https://heroku.com/) support, deploying your project will take under a minute.

## **Installation**

Ready to use **dash-tools**? Installation is easy with pip:

```bash
pip install dash-tools
```

Find [dash-tools on PyPi](https://pypi.org/project/dash-tools/)

## **Usage Examples**

Below are common usage examples. For a more in-depth tutorial on writing apps for Plotly Dash, see the [Plotly Dash Documentation](https://dash.plotly.com/layout). For information about dash-tools commands, read the [_Commands_](#commands) section.

### **Creating A New Project**

Creating a new Dash project is very simple. The following command will create a new directory called "MyDashApp" from where the command is invoked:

```bash
# This command will create the app "MyDashApp" in your current directory.
# MyDashApp will contain all necessary files to make your project
# run, as well as files for deploying to Heroku - see Deploying
# with Heroku in the README below.
dash-tools --init MyDashApp

# You can make changes to your app in the src/app.py file!
# See https://dash.plotly.com/layout
# When you are ready to test it locally you can also run the
# app.py file from terminal:
python MyDashApp/src/app.py

# You can now view the app at http://127.0.0.1:8050/ in your browser.
```

### **Using Templates**

Templates offer different project styles and include different boilerplate code samples. Creating a new app with a template is easy. Just use the optional template argument after `--init`. If you do not specify a template, '_default_' will be used. See the [_Templates_](#templates) section below for more details.

```bash
# Create a new Dash app called "MyWonderfulApp" using 'minimal' template
dash-tools --init MyWonderfulApp minimal
```

To list out available templates, use the `--templates` command:

```bash
# Display available templates
dash-tools --templates

# Note: To see details on each template, check out the 'Templates'
# section in README below.
>>> dash-tools: templates: List of available templates:
>>>         > default
>>>         > tabs
>>>         > sidebar
>>>         > iris
>>>         > multipage
```

### **Deploying with Heroku**

To create a project and deploy to [Heroku](https://www.heroku.com/), it is quite simple. Using the `--deploy-heroku` command in the project root directory will look for the above files. The directory needs to be a git repository, and the [Heroku CLI](https://devcenter.heroku.com/categories/command-line) must be installed.

The command `--deploy-heroku` takes one argument for the project name, which may only contain lowercase, alphanumeric characters and dashes. It must be unique and not already on Heroku. The process will create a new git remote called 'heroku' with the heroku remote url to push/deploy all project code, and will return a URL of your deployed project with the project name you chose, such as [https://your-unique-app-name.herokuapp.com/](#deploying-with-heroku).

```bash
# Create a new app "MyGreatHerokuApp". Any template can be used for this step.
# Procfile and runtime.txt are included with the templates,
# and requirements.txt file will be generated automatically in the next step.
# These files are necessary to deploy to heroku.
dash-tools --init MyGreatHerokuApp

# Change current directory to your new project root directory
cd MyGreatHerokuApp/

# Feel free to make changes to your project at this step!
# See https://dash.plotly.com/layout

# Using the following command will start the deploy process
# Follow the instructions in the console to deploy your app
dash-tools --deploy-heroku your-unique-app-name
```

And that's really it! A new heroku app and git remote will be created, and all project code will be deployed. To push any changes you make after the application is deployed to heroku, create a git commit and push it to the remote heroku branch:

```bash
# Add changes to git staging from the project's root dirctory
git add .

# Create a new commit with a message
git commit -m "Adding some new files"

# Push to the "heroku" remote's "master" branch which was added
# automatically in the example above.
# Your changes will now be sent to heroku, and your app will
# build and be re-deployed automatically.
git push heroku master
```

## **Templates**

Listed below are available project templates. Please see the above [_Using Templates_](#using-templates) section on how to use templates. If you would like to develop templates, please read the [_Creating Templates_](#creating-templates) section below.

- **default** - the default multi-page template. Includes examples of ClientsideCallbacks, multi-page routing, external stylesheets, header, footer, and 404 page.
  ![](docs/default_theme.png)
- **iris** - Iris theme. See [Faculty.ai Example](https://dash-bootstrap-components.opensource.faculty.ai/examples/iris/)
  ![](docs/iris_theme.png)
- **multipage** - New multipage theme. See [Multipage Plugin](https://github.com/plotly/dash-labs/blob/main/docs/08-MultiPageDashApp.md)
  ![](docs/multipage_new_theme.png)
- **sidebar** - Sidebar theme. See [Faculty.ai Example](https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/)
  ![](docs/sidebar_theme.png)
- **tabs** - Tabs theme with dynamically generated content. See [Faculty.ai Example](https://dash-bootstrap-components.opensource.faculty.ai/examples/graphs-in-tabs/)
  ![](docs/tabs_theme.png)

## **Commands**

### **Project Commands**

- **`--deploy-heroku` Args: REQUIRED (`unique heroku project name`) :** Deploys the project to Heroku using the [Heroku CLI](https://devcenter.heroku.com/categories/command-line) (Must Install Seperately) and [Git](https://git-scm.com/downloads). Invoke from the project root directory.
- **`--init, -i` Args: REQUIRED (`project name`) OPTIONAL (`template`) :** Creates a Plotly Dash app with the given name in the current working directory. Optional args specified can be used for templates.
- **`--templates, -t` :** List available templates.

### Other

- **`--help, -h`:** Display CLI helpful hints
- **`--version`:** Display current version.

## **Development**

### **Creating Templates**

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

## **License**

MIT License. See LICENSE.txt file.
