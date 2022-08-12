=======
init
=======

``dashtools init <project name> [project template] [--directory <alternate destination directory>]``


Usage
========

The ``init`` command is used to create a new templated project in the current directory.

.. note::
    See :doc:`Templates <templates>` for information on using Templates.


File Structure
------

The newly created project will look something like this:

.. code-block::

    AppName              [1]
    │-- Procfile
    │-- README.md
    │-- requirements.txt [2]
    │-- runtime.txt
    │
    └── src
        |-- app.py
        |-- __init__.py
        |-- assets/      [3]
        |-- containers/  [3]
        |-- components/  [3]
        └-- data/        [3]

**[1]** Project can be named anything
**[2]** Created during deployment
**[3]** Not included in all templates


Examples
=======

Create a new project named "My-Favorite-App" (app name can be any valid directory name) in the current directory:

.. code-block:: bash

    dashtools init My-Favorite-App

Create a new project using the "multipage" template:

.. code-block:: bash

    dashtools init My-Favorite-App multipage

Create a new project using the "multipage" template in the "apps" directory:

.. code-block:: bash

    dashtools init My-Favorite-App multipage --dir apps
