#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==========================
Test for qplotutils.player
==========================



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

from qplotutils.player import *

__author__ = "Philipp Baust"
__copyright__ = "Copyright 2019, Philipp Baust"
__credits__ = []
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Philipp Baust"
__email__ = "philipp.baust@gmail.com"
__status__ = "Development"

_log = logging.getLogger(__name__)


class PlaybackWidgetTests(unittest.TestCase):

    app = None

    @classmethod
    def setUpClass(cls):
        PlaybackWidgetTests.app = QApplication([])

    def setUp(self):
        config = CONFIG
        config.debug = True
        self.player = PlaybackWidget()

    def test_play(self):
        self.player.timestamps = [0,1,2]
        self.player.play()
        self.player.pause()

        self.player.play()
        self.player.play()

        self.player.pause()
        self.player.pause()

        self.player.play_pause()

        self.player.play()
        self.player.play_pause()

    def test_timestamps(self):
        self.player.timestamps = np.arange(0,100,0.5)
        self.player.jump_to_timestamp("1.5")

    def test_ffwd_bckwd(self):
        self.player.timestamps = np.arange(0, 100, 0.5)
        self.player.jump_to_timestamp("0")


        self.nt = 0
        def _say(idx, ts):
            self.nt = ts
        self.player.timestamp_changed.connect(_say)

        self.player.step_forward()

        self.assertEquals(self.nt, 0.5)


        self.player.step_back()

        self.player.jump_to_timestamp(50)
        self.player.play_pause()
        self.player.play_pause()
        self.player.play_pause()

        self.assertRaises(Exception, self.player.jump_to_timestamp("-3"))

        self.player._slider_pressed()


    def test_without_debug(self):
        CONFIG.debug = False

        p = PlaybackWidget()
        p.timestamps = [0, 1, 2]
        p.play()
        p.pause()