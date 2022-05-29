# **dashtools** Tutorial - _Making Changes and Deploying to Heroku_

> The following tutorial will explain how `dashtools heroku --deploy` works, and how you can use `dashtools heroku --update` to push new changes to your deployed app. Check out the _[Usage Examples](../README.md#usage-examples)_ section in the Readme before you begin.

### Creating an App

1. Create a Dash project in a new directory called "MyApp" (using your terminal or command prompt) using the "sidebar" template:
   <details>
     <summary>Note</summary>
     "MyApp" can be changed to any name. However, for the purpose of this tutorial, we recommend keeping it as "MyApp".
   </details>

   ```bash
   dashtools init MyApp sidebar
   ```

2. Open the default `app.py` file that comes with this project:
   <details>
     <summary>Windows</summary>

   ```bash
    .\MyApp\src\app.py
   ```

   </details>
   <details>
     <summary>Linux and Mac OS</summary>

   ```bash
    ./MyApp/src/app.py
   ```

   </details>

3. Make sure you are in your project's root directory:

   ```bash
   cd MyApp
   ```

4. Run your app to ensure it works:
   <details>
     <summary>Note</summary>
     The run command can be used instead of the traditional "python ./src/app.py" command. In effect, they do the same thing.
   </details>

   ```bash
   dashtools run
   ```

   Visiting http://127.0.0.1:8050/ in your browser will show local changes to the app in real-time

   ![iris image](../docs/templates/sidebar_theme.png)

### Deploy App to Web with Heroku

6. Deploy to Heroku:
   <details>
     <summary>Note</summary>
     The heroku --deploy command creates a new heroku project in your account, adds a git remote called heroku, and pushes changes to the remote. You can use the heroku --update command, discussed below, to push new changes.
   </details>

   ```bash
   dashtools heroku --deploy
   ```

7. Visit your app online to view what it looks like. The URL will be provided when you deploy your app after **Application Page**

![deploy success message](../docs/readme/deploy_success_msg.png)

### Make Changes

8.  Change the tab title

    On line 20, replace `MyApp` in `title="MyApp"` with any name you want. Observe that the tab title in your browser will update automatically

    ```python
    app = dash.Dash(
        title="My Homepage",
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )
    ```

    <details>
    <summary>Receiving a "Site can’t be reached" error?</summary>
    If you receive this error, make sure to correct any python syntax errors you might have and re-run the `dashtools run` command. Since your site is being re-rendered after each change you make, if your app isn't valid python syntax, it will cause this error
    </details>

9.  Change the sidebar

    On line 46, the `sidebar` object defines the layout of the sidebar. Replace the object with the python snippet below to change the name of the sidebar links and title

    ```python
    sidebar = html.Div(
        [
            html.H2("My Site", className="display-4"),
            html.Hr(),
            html.P(
                "Navigation Menu", className="lead"
            ),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("About", href="/about", active="exact"),
                    dbc.NavLink("Contact", href="/contact", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )
    ```

    <details>
    <summary>What happens if you click the About or Contact button?</summary>
    You will also notice an error message in the right hand corner of the screen: "Callback error updating page-content.children".
    <br><br>
    Clicking either of these buttons will try to redirect you to the /about or /contact pages, which have not been created yet. In the next section, we will create those pages. 
    </details>

10. Add an _/about_ and _/contact_ Page

    The `def render_page_content(pathname):` method on line 72 is responsible for routing traffic in your app. Here, we will change `page-1` and `page-2` to work with the Home and About pages, as seen above.

    Copy the following python snippet and replace the `render_page_content` method:

    ```python
    def render_page_content(pathname):
        if pathname == "/":
            return html.P("This is the content of the home page!")
        elif pathname == "/about":
            return html.P("This is your about page!")
        elif pathname == "/contact":
            return html.P("This is your contact page!")
        # If the user tries to reach a different page, return a 404 message
        return html.Div(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )
    ```

    <details>
    <summary>What happens if you click the About or Contact button?</summary>
    Congratulations! Your sidebar buttons will work now as you have linked the navigation links with the new page routing.
    </details>

### Pushing App Changes to Heroku

11. Make sure you are still in your project's root directory "MyApp"

12. After you are happy with your changes and verify that they work in browser, run the following command:

    ```bash
    dashtools heroku --update
    ```

    The command will create a new commit and push it to the _heroku_ remote, created in the deploy step above. After the changes are received by heroku, your project will be re-built and re-deployed to the same web URL as before.

Congratulations, you have successfully made changes and updated your Heroku app!

## More Resources

- [Readme](../README.md)
- [Submit an Issue Ticket](https://github.com/andrew-hossack/dash-tools/issues/new/choose)
- [Troubleshooting](../README.md#troubleshooting)
