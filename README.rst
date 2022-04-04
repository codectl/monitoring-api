******************
monitoring-service
******************

.. image:: https://github.com/rena2damas/monitoring-service/actions/workflows/ci.yaml/badge.svg
    :target: https://github.com/rena2damas/monitoring-service/actions/workflows/ci.yaml
    :alt: CI
.. image:: https://codecov.io/gh/rena2damas/monitoring-service/branch/master/graph/badge.svg
    :target: https://app.codecov.io/gh/rena2damas/monitoring-service/branch/master
    :alt: codecov
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: code style: black
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: license: MIT

A generic monitoring service meant to report on different metrics.

Metrics:

* __health checks__: metrics that assess the status on different services and cluster
components. These metrics are managed and provided by `Bright Computing <https://www
.brightcomputing.com/>`_.

Setup 🔧
=====

The application can run in several ways, depending on what the target platform is.
One can run it directly on the system with ``python``` or get it running on a
``kubernetes`` cluster.

Python
------

The project uses `poetry <https://python-poetry.org/>`_ for dependency management
. Therefore to set up the project (recommended):

.. code-block:: bash

    # ensure poetry is installed
    $ poetry env use python3
    $ poetry install

That will configure a virtual environment for the project and install the respective
dependencies, which is particular useful during development stage.

Kubernetes
----------

Refer to `README <.kustomization/README.rst>`_ under ``.kustomization/``.

Configuration 📄
-------------

Since the project can read properties from the environment, one can use an ``.env``
file for application configurations. These should be set accordingly for a correct
service usage.

A possible configuration is:

.. code-block:: bash

    # Database
    SQLALCHEMY_DATABASE_URI=sqlite:///example.db

    # Application context
    APPLICATION_CONTEXT=/api/monitoring/v1

    # version of OpenAPI
    OPENAPI=3.0.3

    # Bright Computing properties
    BRIGHT_COMPUTING_HOST=brightcomputing.com
    BRIGHT_COMPUTING_PORT=8081
    BRIGHT_COMPUTING_CERT_PATH=etc/ssl/bright/cert.pem
    BRIGHT_COMPUTING_KEY_PATH=etc/ssl/bright/cert.key

    # Supported measurables
    SUPPORTED_MEASURABLES=foo,bar

Note ⚠️: one should use ``configmap`` and ``secret`` instead when configuring it for
``kubernetes``.

Run 🚀
====

For a quick run with ``Flask``, run it like:

.. code-block:: bash

    $ poetry run flask run

Configure ``flask`` environments with environment variables or in a ``.flaskenv`` file.

``Flask`` uses ``Werkzeug`` which is a ``WSGI`` library intended for development
purposes. Do not use it in production! For a production like environment, one should
use instead a production server, like ``gunicorn``:

.. code-block:: bash

    $ poetry run gunicorn src.app:create_app

Tests & linting 🚥
===============

Run tests with ``tox``:

.. code-block:: bash

    # ensure tox is installed
    $ tox

Run linter only:

.. code-block:: bash

    $ tox -e lint

Optionally, run coverage as well with:

.. code-block:: bash

    $ tox -e coverage

License
=======

MIT licensed. See `LICENSE <LICENSE>`_.
