#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==================================
Test for qplotutils.wireframe.view
==================================



Autogenerated package stub.
"""
import unittest
import logging
import sys
import os
import numpy as np

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtOpenGL import *
from qtpy.QtWidgets import *

from qplotutils.wireframe.view import *

__author__ = "Philipp Baust"
__copyright__ = "Copyright 2019, Philipp Baust"
__credits__ = []
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Philipp Baust"
__email__ = "philipp.baust@gmail.com"
__status__ = "Development"

_log = logging.getLogger(__name__)


class ChartView3dTests(unittest.TestCase):

    app = None

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        """ Autogenerated. """
        pass
        
    def test_instantiate(self):
        """ Autogenerated. """
        obj = ChartView3d()  # TODO: may fail!


class ViewPropertiesTests(unittest.TestCase):

    def setUp(self):
        """ Autogenerated. """
        pass
        
    def test_instantiate(self):
        """ Autogenerated. """
        obj = ViewProperties()  # TODO: may fail!