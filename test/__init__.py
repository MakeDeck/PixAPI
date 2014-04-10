"""
Name: Sean Sill
File: __init__.py
Description: Loads all test files in the directory
Taken from:
http://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure
"""

import os
import unittest

__all__ = ['test_service']

def create_test_suite(root='.'):
    module_strings  = find_tests_recursively('test', root)
    print 'Found ', len(module_strings), ' modules.'
    print module_strings
    print 'Attempting to import...'
    suites = [unittest.defaultTestLoader.loadTestsFromName(name) \
          for name in module_strings]
    testSuite = unittest.TestSuite(suites)
    return testSuite

def find_tests_recursively(parent_module, path=None):
    """
    Returns a list of module strings to import
    """
    if path == None:
        return [];
    module_strings = []
    files = os.listdir(path)
    for f in files:
        full_path = os.path.join(path, f)
        if os.path.isfile(full_path):
            if f[:5] == 'test_' and f[-3:] == '.py':
                module_strings.append(parent_module+'.'+f[:len(f)-3])
        elif os.path.isdir(full_path):
            module_strings.extend(
                    find_tests_recursively(parent_module+'.'+f, full_path))
    return module_strings
