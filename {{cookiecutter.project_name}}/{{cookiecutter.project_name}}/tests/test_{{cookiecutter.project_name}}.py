#!/usr/bin/env python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from {{cookiecutter.project_name}} import skeleton


class SkeletonTestCase(unittest.TestCase):
    def setUp(self):
        self.skeleton = skeleton.Skeleton("conf/main.cfg")

    def tearDown(self):
        pass

    def test_attribute(self):
        self.assertEqual(self.skeleton.__class__.__name__, "Skeleton")


if __name__ == "__main__":

    from unittest import TestLoader, TextTestRunner
    suite = TestLoader().loadTestsFromTestCase(SkeletonTestCase)
    TextTestRunner(verbosity=2).run(suite)
