# monitoring-service

A generic monitoring service meant to report on different metrics.

## Metrics:

* __health checks__: metrics that assess the status on different services and cluster components.
  These metrics are managed and provided by [Bright Computing](https://www.brightcomputing.com/).

## Tests & linting

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
