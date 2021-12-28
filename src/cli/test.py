import unittest

import coverage as cv
import click


@click.command(name='test')
@click.option(
    '--coverage/--no-coverage',
    default=False,
    help='Run tests under code coverage.'
)
def test_command(coverage):
    """Run test suite."""
    suite = unittest.TestLoader().discover(start_dir='src/tests')
    runner = unittest.TextTestRunner(verbosity=2)

    cov = cv.Coverage()
    cov.start()
    runner.run(suite)
    cov.stop()

    if coverage:
        cov.report()
