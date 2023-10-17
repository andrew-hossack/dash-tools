.. image:: _static/images/logo_bk.png
   :align: center
   :class: only-light

.. image:: _static/images/logo_w.png
   :align: center
   :class: only-dark

|

DashTools is an open-source command line toolchain for `Plotly Dash <https://dash.plotly.com/introduction>`_ that makes creating and deploying dash projects to `Heroku <https://heroku.com/>`_ intuitive and easy.


Use dashtools to...
--------------
- **Create templated dash apps** with one command
- **Deploy your app** to Heroku and Render in under a minute
- **Generate Procfile, requirements.txt and runtime.txt** automatically on deploy
- **Many boilerplate templates** for creating apps
- **Dockerize your app** in a single step


Getting started
--------
To get started using dashtools, check out the :doc:`Getting Started <getting started>` page.

Install with:

.. code-block:: bash
   
   pip install dash-tools

Run the dashboard with:

.. code-block:: bash

   dashtools gui

Create projects with:

.. code-block:: bash

   dashtools init <app name>

Pages
-------

.. toctree::
    :maxdepth: 1

    getting started
    commands/index
    tutorials/index

.. toctree::
    :caption: Development
    :maxdepth: 1

    changelog
    contributing
    issues
    license
