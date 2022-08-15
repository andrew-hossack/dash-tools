# Usage Examples

Example A assumes you already have a functioninig app that you would like to deploy to the web. If you do not have an app and would like to start with a dash-tools template that contains a sample app, jump to [Example B](#b-create-an-app).

### A. Deploying and Updating a Deployed App with Heroku

#### Deploying an App

1. Make sure you are in your project's root directory. For example, your project folder structure might look like this:

   ```
   MyApp
   └── src
       |-- app.py
       └── ...
   ```

   In your terminal or command prompt, replace "MyApp" below with the root directory name of your project, and go into that directory:

   ```bash
   cd MyApp
   ```

2. If you did not [create a boilerplate app](#b-create-an-app) using dashtools, you must verify that your app is ready to be deployed to Heroku:

   - Your project must contain an **app.py** file

   - Your **app.py** file must contain a `server` variable after your initialize your app:

   ```python
   app = Dash(__name__)
   server = app.server
   ```

3. If your app has local csv or excel sheets, read below. Otherwise, skip to step 4.
   <details>
     <summary>Requirements</summary>

   A. Your project folder structure should have a data folder that contains the csv/excel sheet. For example:

   ```
   MyApp
   |── src
   |   |-- app.py
   |   └── ...
   └── data
       └── YourCsvFileName.csv
   ```

   B. When loading in CSV data, make sure to use the correct path to the data file, as seen below:

   ```python
   import pandas as pd
   import pathlib

   def get_pandas_data(csv_filename: str) -> pd.DataFrame:
      '''
      Load data from /data directory as a pandas DataFrame
      using relative paths. Relative paths are necessary for
      data loading to work in Heroku.
      '''
      PATH = pathlib.Path(__file__).parent
      DATA_PATH = PATH.joinpath("data").resolve()
      return pd.read_csv(DATA_PATH.joinpath(csv_filename))

   my_csv_dataframe = get_pandas_data("MyCSVFile.csv")
   ```

   </details>

4. Verify that running your app locally produces no errors

5. Deploying to Heroku is made simple with the following command:

   ```bash
   dashtools heroku --deploy
   ```

#### Updating an App

Updates can only be pushed to projects that are already deployed on Heroku via above example [Deploying an App](#deploying-an-app).

6. From the project's root directory, or the "MyApp" directory in the example above, run the following update command to push all changes to your deployed Heroku app:

   ```bash
   dashtools heroku --update
   ```

### B. Create an App

1. Create a Dash project in a new directory called "MyDashApp" (using your terminal or command prompt):
   <details>
     <summary>Naming Note</summary>
     "MyDashApp" can be changed to any name. However, for the purpose of this tutorial, we recommend keeping it as "MyDashApp".
   </details>

   ```bash
   dashtools init MyDashApp
   ```

2. Open the default `app.py` file that comes with this project:
   <details>
     <summary>Windows</summary>

   ```bash
    .\MyDashApp\src\app.py
   ```

   </details>
   <details>
     <summary>Linux and Mac OS</summary>

   ```bash
    ./MyDashApp/src/app.py
   ```

   </details>

3. Replace the code in `app.py` with your own app code. Make sure to keep the `server = app.server` right after app instantiation:

![update-app](https://user-images.githubusercontent.com/32049495/169304171-bf23b2d0-26b4-4767-b38f-cd6586ddf56e.gif)

4. Make sure you are in your project's root directory:

   ```bash
   cd MyDashApp
   ```

5. Run your app to ensure it works:

   Linux and Mac OS

   ```bash
   python src/app.py
   ```

   Windows

   ```bash
   python src\app.py
   ```
