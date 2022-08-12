=======
Run
=======

``dashtools run [--set-py-cmd <shell command>]``


Usage
========

The ``run`` command is used to run the app.py file. It searches recursively through current directory for app.py file. If none is found, look for a Procfile to point to the main application file. 

The ``--set-py-cmd`` option can be used to set the python command to use when running the app; eg. ``--set-py-cmd python3``.


Examples
=======

Run the app.py file in the current directory:

.. code-block:: bash

    dashtools run


Set the python command to use when running the app to python3.exe:

.. code-block:: bash

    dashtools run --set-py-cmd python3.exe

