=======
templates
=======

``dashtools templates [--list] [--init <directory to convert>]``


Usage
-----

Templates are pre-configured dashboards that can be used to quickly create new dash projects.


templates --list
===============

``dashtools templates --list``

Usage
-----

List all available templates.


Examples
--------

.. code-block:: bash
    dashtools templates --list

templates --init
===============

``dashtools templates --init <directory to convert>``

Usage
-----

Convert directory to a dashtools project template. Files with {appName} string will be converted to the project name when ``dashtools init <app name>`` is used. Additionally, {createTime} will be replaced with the current time.

Examples
--------

Convert the my-app directory to a dashtools project template:

.. code-block:: bash
    dashtools templates --init my-app

