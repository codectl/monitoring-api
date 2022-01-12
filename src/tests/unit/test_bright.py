import unittest


class TestApp(unittest.TestCase):

    def setUp(self):
        self.bright = Bright(version='latest')
        bright.health_checks()

    def tearDown(self):
        pass
