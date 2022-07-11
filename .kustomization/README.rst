*************
Kustomization
*************

Refer to the `main <https://github.com/rena2damas/microservices.git#kustomization>`_
repository.

Directory structure
===================

Refer to the
`main <https://github.com/rena2damas/microservices.git#directory-structure>`_
repository.

Secret management
=================

There are no secrets needed to manage on this project.

Usage
=====

Refer to the `main <https://github.com/rena2damas/microservices.git#usage>`_ repository.

Upon following those steps, the ``pods`` should be running (or about to). An example
output with default settings:

.. code-block:: bash

    $ kubctl get pods
    NAME                       READY   STATUS      RESTARTS    ...
    monitoring-api-XXX-XXX     1/1     Running     0           ...
    monitoring-api-XXX-XXX     1/1     Running     0           ...
