#!/usr/bin/python
"""
Chart01
-------


"""
import os
import signal
import sys
import numpy as np
from qtpy.QtCore import QTimer
from qtpy.QtWidgets import QApplication


PKG_DIR = os.path.abspath(os.path.join(__file__, "..", ".."))
print(PKG_DIR)
if PKG_DIR not in sys.path:
    sys.path.append(PKG_DIR)


from qplotutils import Configuration
from qplotutils.chart.view import ChartView
from qplotutils.chart.items import LineChartItem


__author__ = "Philipp Baust"
__copyright__ = "Copyright 2015, 2017, Philipp Baust"
__credits__ = []
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Philipp Baust"
__email__ = "philipp.baust@gmail.com"
__status__ = "Development"



if __name__ == "__main__":
    """ Minimal example showing a bench with 2 docks.
    The docks can be resized and dragged around.
    """

    cfg = Configuration()
    cfg.debug = True


    def sigint_handler(signum, frame):
        """ Install handler for the SIGINT signal. To kill app through shell.

        :param signum:
        :param frame:
        :return:
        """
        # sys.stderr.write('\r')
        QApplication.exit()


    signal.signal(signal.SIGINT, sigint_handler)

    qapp = QApplication([])

    # call the python loop periodically to catch interrupts from shell
    timer = QTimer()
    timer.start(1000)
    timer.timeout.connect(lambda: None)

    view = ChartView(orientation=ChartView.CARTESIAN)
    view.resize(800, 400)

    l = LineChartItem()
    x = np.arange(-30, 300, 0.2, dtype=np.float)
    y = np.sin(2 * np.pi * 3 / float(max(x) - min(x)) * x)
    l.plot(y, x, "a sine")
    view.addItem(l)

    view.autoRange()
    view.show()
    qapp.exec_()