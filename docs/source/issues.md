# Troubleshooting

## Bugs

If you find any bugs or issues, please report them directly to the [GitHub Issue Tracker](https://github.com/andrew-hossack/dash-tools/issues/new/choose).

## Common Solutions

Running into issues? Outlined below are common errors and solutions.

Please make sure you are running the latest version of dash-tools: `python -m pip install --upgrade dash-tools` first. If you do not find an answer below, please [Submit an Issue Ticket](https://github.com/andrew-hossack/dash-tools/issues/new/choose).

<details><summary>Command 'dashtools' is not recognized (windows)</summary>

_Problem:_ You encounter an error "The term 'dashtools' is not recognized as the name of a cmdlet, function, script file, or operable program" when trying to run the dashtools command on Windows.

_Solution:_ Run the command with .\dashtools instead. You may need to add dashtools to your system path variables.

</details>

<details><summary>Common heroku --deploy Issues</summary>

<details><summary>&ensp;&ensp;&ensp;&ensp;Error when creating requirements.txt file</summary>

_Problem:_ You encounter an error when generating a requirements.txt file

_Solution:_ Verify that you are running the `dashtools heroku --deploy` command from a valid plotly dash app directory. E.g. there is a `src/app.py` file.

</details>

<details><summary>&ensp;&ensp;&ensp;&ensp;No webpage displayed after Heroku deployment, no error messages</summary>

_Problem:_ You are able to deploy your project online to Heroku, but nothing is displayed on the page

_Solution1:_ This may be due to missing libraries that your app needs to run successfully. Check the requirements.txt. file.

_Solution2:_ This may due to the fact that you forgot to add `server = app.server` to you main app.py file

</details>

<details><summary>&ensp;&ensp;&ensp;&ensp;Procfile is incorrect</summary>

_Problem:_ When deploying, you get an error "Procfile is incorrect"

_Solution:_ When deploying an app, the Procfile is checked for validity. Make sure that your Procfile points to the correct server entrypoint, e.g. `server = app.server`.

</details>
   
<details><summary>&ensp;&ensp;&ensp;&ensp;No solution found</summary>

_Solution:_ Try typing into the terminal or command prompt `heroku logs --tail`. This will give you access to the official heroku logs of your app that enable monitoring your stack error troubleshooting

</details>

</details>

<details><summary>Common heroku --update Issues</summary>

<details><summary>&ensp;&ensp;&ensp;&ensp;Your account has reached its concurrent build limit.</summary>

_Problem:_ When you try to update and redeploy your app to Heroku too many times within 10 minutes, you will get the above error message

_Solution:_ First, wait a few minutes and try again. If that doesn't work, check out a few possible solutions [in this thread](https://stackoverflow.com/questions/47028871/heroku-your-account-has-reached-its-concurrent-build-limit).

</details>

<details><summary>&ensp;&ensp;&ensp;&ensp;Unable to update heroku app</summary>

_Problem:_ When you try to update your app, you get an error "Unable to update heroku app. Is the project already deployed?"

_Solution:_ Make sure you have already run `git init` in the project root directory, and that you have already followed steps to deploy your project to heroku with `dashtools heroku --deploy`

If both of these steps do not work, verify that the `heroku` remote was added by running `git remote`. If you do not see it, try re-deploying your app or manually push to the correct remote with the `dashtools heroku --update <remote>` option, where `<remote>` is replaced with the correct remote.

</details>

</details>

<details><summary>Common init Issues</summary>

<details><summary>&ensp;&ensp;&ensp;&ensp;No write permission</summary>

_Problem:_ You receive a 'write permission' error while trying to init a new app

_Solution:_ Please check your write permissions for the current directory. Try the init command from a different directory.

</details>

</details>

<details><summary>Common run Issues</summary>

<details><summary>&ensp;&ensp;&ensp;&ensp;No valid python command found for your system</summary>

_Problem:_ You encounter an error: No valid python command found for your system when trying to run your app

_Solution:_ Set the python shell command with "dashtools run --set-python-shell-cmd <command>". The correct command will be the python command that runs python, eg. python, python.exe, python3, python3.exe on your system. Note that although you may be able to run 'python' from your terminal, this may be an alias command for your terminal, and not the correct command.

</details>

<details><summary>&ensp;&ensp;&ensp;&ensp;No such file or directory</summary>

_Problem:_ You encounter an error: 'No such file or directory' when trying to `dashtools run` your app

_Solution:_ Verify that you are running the `dashtools run` command from within a valid project root directory. Your app must be named `app.py`, or have a valid Procfile pointing to the app file.

</details>

<details><summary>&ensp;&ensp;&ensp;&ensp;Invalid Procfile</summary>

_Problem:_ When you try to run, you get an error "Invalid Procfile"

_Solution:_ When you run an app, the Procfile is checked for validity. Make sure that your Procfile points to the correct server entrypoint, e.g. `server = app.server`.

</details>

</details>
