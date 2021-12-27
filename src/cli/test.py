import unittest

import coverage
import click


@click.command()
@click.option(
    '--coverage/--no-coverage',
    default=False,
    help='Run tests under code coverage.'
)
def test_command(cvg):
    """Run test suite."""
    suite = unittest.TestLoader().discover(start_dir='tests')
    runner = unittest.TextTestRunner(verbosity=2)

    if cvg:
        cov = coverage.Coverage()
        cov.start()
        runner.run(suite)
        cov.stop()
        cov.report()
    else:
        runner.run(suite)
