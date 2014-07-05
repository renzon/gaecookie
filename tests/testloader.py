#!/usr/bin/env python
# coding: utf-8

import unittest
import sys
import os

ROOT_PATH = os.path.dirname(__file__)

if __name__ == '__main__':
    if 'GAE_SDK' in os.environ:

        SDK_PATH = os.environ['GAE_SDK']

        sys.path.insert(0, SDK_PATH)

        import dev_appserver
        dev_appserver.fix_sys_path()


    tests = unittest.TestLoader().discover(ROOT_PATH, "*tests.py")
    result = unittest.TextTestRunner().run(tests)

    if not result.wasSuccessful():
        sys.exit(1)
