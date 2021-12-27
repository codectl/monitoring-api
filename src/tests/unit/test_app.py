import unittest

from src.app import create_app


class TestApp(unittest.TestCase):

    def test_can_create_app(self):
        """Can create an app."""
        app = create_app()

        self.assertTrue(app)
