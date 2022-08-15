=======
templates --init
=======

Convert directory to a dashtools project template. 

Files with {appName} string will be converted to the project name when ``dashtools init <app name>`` is used. Additionally, {createTime} will be replaced with the current time.
    
Usage
======
    
``dashtools templates --init <directory to convert>``

Examples
=========

Convert the my-app directory to a dashtools project template:

.. code-block:: bash

    dashtools templates --init my-app

