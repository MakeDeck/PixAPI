"""
Testing Helpers for eido

"""

import unittest

class EidoTestCase(unittest.TestCase):
    def setUp(self):
        modules = self.id().split('.')
        print '\nIn Module: ', modules[-2], ' TestCase: ', modules[-1]

