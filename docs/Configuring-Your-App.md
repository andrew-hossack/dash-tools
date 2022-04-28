# 🛠️ **dash-tools** Tutorial - _Create and Upload Your App_

The following sections will provide a beginner guide on how to modify your dash-tools project. This is a beginner tutorial, so more advanced topics such as [callbacks](https://dash.plotly.com/basic-callbacks) will not be discussed. Check out the [Plotly Dash Documentation](https://dash.plotly.com/) for more detailed information on dash features.

## 1. Creating Your App

> _Already have a plotly dash project you want to publish to Heroku? Check out the [Uploading an Existing App](#41-optional-uploading-an-existing-app) section!_

Welcome to the Plotly Dash and dash-tools tutorial! If you are like me, you are interested in learning how Dash can be useful for creating Python data-vis applications (or any type of web app). On its own, Plotly Dash provides a very simple framework for making that happen. With dash-tools, most of the boilerplate dash code is handled for you, making it easier to create amazing apps with even fewer keystrokes.

Let's begin. We are going to create a new dash application called "MyApp". When you create an app, a directory will be created from where you call the command.

**To create the app, type the following command in your console:**

```bash
dash-tools --init MyApp
```

The newly created "MyApp" directory will look something like this:

```
MyApp
│-- README.md
│-- Procfile
│-- runtime.txt
│
└───src
    |-- __init__.py
    └-- app.py
```

Don't know what the files are? That's okay, we will get to that later in the [Project Files](#5-additional-info---project-files) section. First, we will run the dash app locally in your browser to see what it looks like!

## 2. Running Your App

> _Running your app in-browser is the best way to make sure everything works correctly. You can even see changes in real time!_

Let's run your newly created dash application to see what is looks like. The main application file is called `app.py` located in the `src` folder in your MyApp project.

**To see your project in browser, type the following command in your console:**

```bash
cd MyApp
python src/app.py
```

The output of the second command will look something like this:

```
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
```

Navigate to [http://127.0.0.1:8050/](http://127.0.0.1:8050/) in your browser to view your app. Any changes (or errors) you make to the project will be displayed in real-time here! Next, we will be exploring how to make changes to your new app.

## 3. Changing Your App

> _Making changes to your app is easy. Make sure to have the application running in your browser to view any changes you make._

Congrats! If you have made it this far, you were able to create and view a python web application! Feel free to give yourself a pat on the back and grab a coffee for the troubles. In this section, we will talk about what the included project files are for, and how to change your application to make it your own.

Let's start by looking in the `src/app.py` file. As mentioned below in the [Additional Info - Project Files](#5-additional-info---project-files) section, this file is the main dash application file. Any changes you make here will affect the layout of your application.

**To change your application header and text, open your src/app.py file and make the following changes to app.layout:**

```
app.layout = html.Div(children=[
    html.H1(children='Hey There! I'm a new header!'),

    html.Div(children='''
        I can add any text that I want here.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
```

With the magic of programming, you will see the new header and text appear in real time in your browser. Cool, right? If you want to learn more about how you can modify your app in better detail, check out the [Plotly Dash Docs](https://dash.plotly.com/layout)!

> _Note: `server = app.server` in your `src/app.py` file is necessary to upload to Heroku - do not change this!_

Now that you made some changes, let's publish them online to Heroku.

## 4. Deploy to Heroku

> _Heroku is an application host. By hosting your app on Heroku, you will be able to access it from anywhere with an internet connection!_

Stick in there - you're doing great! Let's publish your changes online with Heroku. Like the idea of having a free python webhost? Me too!

Begin by creating a Heroku Account if you have not done so already: [Heroku Account Signup](https://signup.heroku.com/login). To upload your dash-tools application, run the following commands from the root of your MyApp directory.

**Your project needs to be a git repository, type the following command in your console:**

```bash
git init
```

**Next, to begin the upload process, type the following command in your console:**

```bash
dash-tools --deploy-heroku
```

You will be prompted to choose either a unique Heroku name with the following criteria or have one generated for you. If you choose to create a name, make sure that:

- Name is unique (not already taken)
- At least 3 characters long
- Starts with a letter, ends with a letter or digit
- Only contains lowercase letters
- Only contains letters, numbers and dashes

That's really it. After you follow the on-screen instructions, your app will be uploaded for you, and you will be able to view it online!

### 4.1 (Optional) Uploading an Existing App

Uploading an existing application without using a dash-tools template is easy. You need to make sure of the following:

- Your project contains `src/app.py` application file
- Your `src/app.py` file contains the `server = app.server` declaration for heroku

Since the deploy command will create your Procfile, runtime.txt and requirements.txt files for you, there is no need to worry about creating them yourself.

To deploy, the next steps will be the same [as above](#4-deploy-to-heroku).

## 5. Additional Info - Project Files

As shown above in the [Creating Your App](#1-creating-your-app) section, the project directory contains boilerplate files:

#### **Dash Files:**

These files are necessary for your app to run.

- `src/__init__.py` - _Declares the src directory as a python module_
- `src/app.py` - _Main dash application file_

#### **Heroku Files:**

Files that are necessary to deploy your project to Heroku.

- `Procfile` - _Specifies the commands that are executed by the app on Heroku startup_
- `runtime.txt` - _Declares the python runtime version for heroku_

> In the [Deploy to Heroku](#4-deploy-to-heroku) section, another necessary file will be generated automatically for you that isn't already included:
>
> `requirements.txt` **(Not Created Yet)** - _List of required packages to include for Heroku_

#### **Other Files:**

Other files that are not required by either dash or Heroku.

- `README.md`
  - Markdown documentation file
