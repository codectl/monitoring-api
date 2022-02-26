# monitoring-service

A generic monitoring service meant to report on different metrics.

## Metrics:

* __health checks__: metrics that assess the status on different services and cluster components. These metrics are
  managed and provided by [Bright Computing](https://www.brightcomputing.com/).

## Project setup 🔧

The application can run in several ways, depending on what the target platform is. One can run it directly on the system
with```python``` or get it running on a ```kubernetes``` cluster.

### Python

The project uses [poetry](https://python-poetry.org/) for dependency management, therefore to set up the project (
recommended):

```bash
$ poetry env use python3
$ poetry install
```

That will configure a virtual environment for the project and install the respective dependencies. This approach is
particular useful during development stage.

### Configuration 📄

Since the project can read properties from the environment, one can use an ```.env``` file for application
configurations. These should be set accordingly for a correct service usage.

A possible configuration is:

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

Note ⚠️: one should use ```configmap``` and ```secret``` instead when setting it up with ```kubernetes```.

# Run 🚀



## Tests & linting 🚥

Run tests with ```tox```:

```bash
# ensure tox is installed
$ tox
```

Run linter only:

```bash
$ tox -e lint
```

Optionally, run coverage as well with:

```bash
$ tox -e coverage
```

## License

MIT licensed. See [LICENSE](LICENSE).
