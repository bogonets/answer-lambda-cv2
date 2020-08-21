# -*- coding: utf-8 -*-

import importlib.util
import unittest


def import_module(name):
    spec = importlib.util.spec_from_file_location(name, f'{name}.app.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cv2_orb_detect = import_module('cv2_orb_detect')


class TestNumpyLambdas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_orb(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
