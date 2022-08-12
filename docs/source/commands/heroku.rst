=======
heroku
=======

``dashtools heroku [--deploy [optional app name]] [--update [heroku remote name]]``

Usage
-----

Handle deploying and updating your app to Heroku.


heroku --deploy
================

``dashtools heroku --deploy [optional app name]``


Usage
-----

Deploy your app to Heroku from the project root directory.

Examples
--------

Deploy project to Heroku from the project root directory:

.. code-block:: bash

    dashtools heroku --deploy


heroku --update
================

``dashtools heroku --deploy [optional app name]``

Usage
-----

Update a previously deployed app from the project root directory.

Examples
--------

Update project from the project root directory:

.. code-block:: bash

    dashtools heroku --update

If your Heroku remote isn't named "heroku", you can specify the name of the remote to update:

.. code-block:: bash

    dashtools heroku --update myremote

"""

