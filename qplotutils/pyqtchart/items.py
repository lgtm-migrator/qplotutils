import numpy as np
import logging
import itertools
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from . import DEBUG, LOG_LEVEL
from .utils import makePen

__author__ = "Philipp Baust"
__copyright__ = "Copyright 2015, 2017, Philipp Baust"
__credits__ = []
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Philipp Baust"
__email__ = "philipp.baust@gmail.com"
__status__ = "Development"


_log = logging.getLogger(__name__)
_log.setLevel(LOG_LEVEL)


class ChartItemFlags(object):
    FLAG_NO_AUTO_RANGE = 1
    FLAG_NO_LABEL = 2


class BaseMixin(object):

    def __init__(self, parent=None):
        """ Base mixin for all items that are placed on the chart view.

        :param parent: Parent QGraphicsItem, QGraphicsItemGroup or QGraohicsItemWidget
        """
        super(BaseMixin, self).__init__(parent=parent)
        self.__flags = 0

    def visibleRangeChanged(self, rect):
        """ Slot that is called when the chart view visible range changed.

        :param rect: The visible rectangle
        """
        pass

    @property
    def chartItemFlags(self):
        """ Returns the ChartItemFlags for this chart item

        :return: flags
        """
        return self.__flags

    @chartItemFlags.setter
    def chartItemFlags(self, flags):
        self.__flags = flags

    @property
    def color(self):
        """ The items plot color.

        :return: color
        """
        return QColor("#FFFFFF")

    @property
    def label(self):
        """ Label of the item.

        :return: label
        """
        return "-"


class ChartItemGroup(BaseMixin, QGraphicsItemGroup):

    def __init__(self, parent=None):
        """ Item group for chart view items

        :param parent:
        """
        super(ChartItemGroup, self).__init__(parent=parent)

    def __repr__(self):
        return "<ChartItemGroup>"

    def __del__(self):
        _log.debug("Finalizing: {}".format(self))


class ChartWidgetItem(BaseMixin, QGraphicsWidget):

    def __init__(self, parent=None):
        """

        :param parent:
        """
        super(ChartWidgetItem, self).__init__(parent=parent)

    def __repr__(self):
        return "<ChartWidget>"

    def __del__(self):
        _log.debug("Finalizing: {}".format(self))


class ChartItem(BaseMixin, QGraphicsItem):

    def __init__(self, parent=None):
        super(ChartItem, self).__init__(parent=parent)
        self.b_rect = QRectF(0, 0, 1, 1)

        # self._flags = 0

    def boundingRect(self):
        # Override
        return self.b_rect

    def paint(self, p=QPainter(), o=QStyleOptionGraphicsItem(), widget=None):
        # Override
        if DEBUG:
            p.setPen(QPen(Qt.blue))
            p.drawRect(self.b_rect)

    def __repr__(self):
        return "<ChartItem>"

    def __del__(self):
        _log.debug("Finalizing: {}".format(self))


class TextItem(ChartItem):
    def __init__(self, pos, text, parent=None):
        super(TextItem, self).__init__(parent)
        self.setFlags(QGraphicsItem.ItemIgnoresTransformations)
        self.chartItemFlags = ChartItemFlags.FLAG_NO_LABEL

        # self._topLeft = QPointF(0,0) # topLeftPosition
        self._text = QStaticText(text)
        self._bRectF = QRectF(QPointF(0, 0), self._text.size())
        self.font = QFont("Helvetica [Cronyx]", 12, QFont.Normal)
        self.font_flags = Qt.TextDontClip | Qt.AlignRight | Qt.AlignVCenter

        self.setPos(pos)

    def boundingRect(self):
        return QRectF(QPointF(0, 0), self._text.size())

    def paint(self, p=QPainter(), o=QStyleOptionGraphicsItem(), widget=None):
        p.setPen(QPen(self.color))
        p.setFont(self.font)
        p.drawStaticText(QPointF(0, 0), self._text)


class WireItem(ChartItem):
    def __init__(self, parent=None):
        super(WireItem, self).__init__(parent)

    def boundingRect(self):
        return QRectF(QPointF(0, -100), QSizeF(200, 200))

    def paint(self, p=QPainter(), o=QStyleOptionGraphicsItem(), widget=None):
        pen = QPen(Qt.blue)
        p.setPen(pen)
        p.drawRect(QRectF(QPointF(0, -100), QSizeF(200, 200)))


class CoordCross(ChartItem):

    def __init__(self, parent=None):
        super(CoordCross, self).__init__(parent)

    def boundingRect(self):
        return QRectF(-9, -9, 18, 18)

    def paint(self, p=QPainter(), o=QStyleOptionGraphicsItem(), widget=None):
        pen = QPen(Qt.red)
        p.setPen(pen)

        p.drawLine(QLineF(0, 0, 2, 0))
        p.drawLine(QLineF(2, 0, 1.5, 0.5))
        p.drawLine(QLineF(2, 0, 1.5, -0.5))

        pen = QPen(Qt.blue)
        p.setPen(pen)
        p.drawLine(QLineF(0, 0, 0, 2))
        p.drawLine(QLineF(0, 2, 0.5, 1.5))
        p.drawLine(QLineF(0, 2, -0.5, 1.5))

        pen = QPen(Qt.yellow)
        p.setPen(pen)
        p.drawRect(-9, -9, 18, 18)


class LineChartItem(ChartItem):
    """ Visualises the given data as line chart. """

    def __init__(self, parent=None):
        super(LineChartItem, self).__init__(parent)
        self._xData = None
        self._yData = None
        self._label = None
        self._color = None
        self._bRect = None
        self.markers = {}

        self._showticks = False
        self._visible_range = None

        self._ordinate = None
        self._abscissa = None
    #     self._column = None
    #
    # @property
    # def column(self):
    #     return self._column

    @property
    def ordinate(self):
        return self._ordinate

    @ordinate.setter
    def ordinate(self, value):
        self._ordinate = value

    @property
    def abscissa(self):
        return self._abscissa

    @abscissa.setter
    def abscissa(self, value):
        self._abscissa = value

    @property
    def showTicks(self):
        return self._showticks

    @showTicks.setter
    def showTicks(self, value):
        self._showticks = value
        self.visibleRangeChanged(self._visible_range)

    @property
    def color(self):
        return self._color

    @property
    def label(self):
        return self._label

    def plot(self, data, index=None, label=None, color=QColor(Qt.red)):
        self._yData = data

        if index is not None:
            self._xData = index
        else:
            self._xData = np.arange(len(data))

        if label is not None:
            self._label = label

        self._color = color

        self._bRect = QRectF(QPointF(np.min(self._xData), np.min(self._yData)),
                             QPointF(np.max(self._xData), np.max(self._yData)))
        # _log.debug("Plot BB: {}".format(self._bRect))
        #
        # # TODO: Public access
        # self.canvas._items.append(self._bRect)

        self._makePath()

    def _makePath(self):
        self._path = QPainterPath()
        self._path.moveTo(self._xData[0], self._yData[0])

        for k, idx in enumerate(self._xData):
            d = self._yData[k]
            self._path.lineTo(idx, d)

    def boundingRect(self):
        """ Returns the bounding rect of the chart item
        :return: Bounding Rectangle
        :rtype: QRectF
        """
        return self._bRect

    def paint(self, p=QPainter(), o=QStyleOptionGraphicsItem(), widget=None):
        # _log.debug("LCI: paint")
        pen = makePen(self.color)
        p.setPen(pen)

        if self._path:
            p.drawPath(self._path)

        # if any(self.markers):
        #     # pen = makePen(Qt.yellow)
        #     # p.setPen(pen)
        #     # p.drawRects(self.markers)
        #
        #     for m in self.markers:
        #         marker = RectMarker(m)
        #         marker.setParentItem(self)


        if DEBUG:
            p.setPen(Qt.yellow)
            p.drawRect(self._bRect)


    def visibleRangeChanged(self, rect=QRectF()):
        _log.debug("Visible range changed to: {}".format(rect))
        self._visible_range = rect

        visible_indices = np.where(np.logical_and(
            np.logical_and(self._xData >= rect.left(),
                           self._xData <= rect.right()),
            np.logical_and(self._yData >= rect.top(),
                           self._yData <= rect.bottom())))[0]

        # _log.debug("Visible plot points idx: {}".format(visible_indices))

        # self.markers = []
        if len(visible_indices) < 400 and self.showTicks:
            # _log.debug("Too many indices for display")
            # return

            # self.markers = [QPointF(self._xData[idx], self._yData[idx]) for idx in visible_indices]
            _log.debug("Making markers")
            for idx in visible_indices:
                if idx not in self.markers:
                    pos = QPointF(self._xData[idx], self._yData[idx])
                    marker = RectMarker(pos)
                    self.markers[idx] = marker
                    marker.setParentItem(self)


        else:
            _log.debug("removing all markers")
            for k in self.markers:
                item = self.markers[k]
                self.scene().removeItem(item)
                # del self.markers[k]
            self.markers = {}

    def __del__(self):
        _log.debug("Finalize Linechart {}".format(self))


class RectMarker(ChartItem):

    def __init__(self, pos, parent=None):
        super(RectMarker, self).__init__(parent)
        self.setFlags(QGraphicsItem.ItemIgnoresTransformations)

        self.setPos(pos)

    def boundingRect(self):
        return QRectF(-2, -2, 4, 4)

    def paint(self, p=QPainter(), o=QStyleOptionGraphicsItem(), widget=None):

        p.setPen(QPen(Qt.white))
        p.drawRect(QRectF(-2, -2, 4, 4))


class ColorSet(object):
    """ Collection if color sets.
    All generated by http://colorbrewer2.org/
    """

    @classmethod
    def Default(cls):
        """ Default set: 9 colors should be printer friendly """
        return itertools.cycle([
            QColor(228, 26, 28),
            QColor(55, 126, 184),
            QColor(77, 175, 74),
            QColor(152, 78, 163),
            QColor(255, 127, 0),
            QColor(255, 255, 51),
            QColor(166, 86, 40),
            QColor(247, 129, 191),
            QColor(153, 153, 153),
        ])


    @classmethod
    def QualitativePaired(cls):
        """ Set with 12 colors """
        return itertools.cycle([
            QColor(166, 206, 227),
            QColor(31, 120, 180),
            QColor(178, 223, 138),
            QColor(51, 160, 44),
            QColor(251, 154, 153),
            QColor(227, 26, 28),
            QColor(253, 191, 111),
            QColor(255, 127, 0),
            QColor(202, 178, 214),
            QColor(106, 61, 154),
            QColor(255, 255, 153),
            QColor(177, 89, 40),
        ])


    @classmethod
    def Qualitative(cls):
        """ Another set with 12 colors """
        return itertools.cycle([
            QColor(166, 206, 227),
            QColor(31, 120, 180),
            QColor(178, 223, 138),
            QColor(51, 160, 44),
            QColor(251, 154, 153),
            QColor(227, 26, 28),
            QColor(253, 191, 111),
            QColor(255, 127, 0),
            QColor(202, 178, 214),
            QColor(106, 61, 154),
            QColor(255, 255, 153),
            QColor(177, 89, 40),
        ])


    @classmethod
    def Stupid(cls):
        """ First try not the best, since sequential. """
        return itertools.cycle([
            QColor("#a6cee3"),
            QColor("#1f78b4"),
            QColor("#b2df8a"),
            QColor("#33a02c"),
            QColor("#fb9a99"),
            QColor("#e31a1c"),
            QColor("#fdbf6f"),
            QColor("#ff7f00"),
            QColor("#cab2d6"),
            QColor("#6a3d9a"),
            QColor("#ffff99"),
            QColor("#b15928"),
        ])


class HLine(ChartItem):

    def __init__(self, parent=None):
        super(HLine, self).__init__(parent)
        self._y = None

        self._label = None
        self._color = None
        self._bRect = None

        self.chartItemFlags = ChartItemFlags.FLAG_NO_LABEL | ChartItemFlags.FLAG_NO_AUTO_RANGE

    @property
    def color(self):
        return self._color

    @property
    def label(self):
        return self._label

    def setY(self, y, label=None, color=QColor(Qt.red)):
        self._y = y

        if label is not None:
            self._label = label

        self._color = color

        finfo = np.finfo(np.float32)

        self._bRect = QRectF(QPointF(finfo.min, y + 1),
                             QPointF(finfo.max, y - 1),)
        self._makePath()

    def _makePath(self):

        finfo = np.finfo(np.float32)

        self._path = QPainterPath()
        self._path.moveTo(finfo.max, self._y)
        self._path.lineTo(finfo.min, self._y)

    def boundingRect(self):
        """ Returns the bounding rect of the chart item
        :return: Bounding Rectangle
        :rtype: QRectF
        """
        return self._bRect

    def paint(self, p=QPainter(), o=QStyleOptionGraphicsItem(), widget=None):
        # _log.debug(": paint")
        pen = makePen(self.color)
        p.setPen(pen)

        if self._path:
            p.drawPath(self._path)

    def __del__(self):
        _log.debug("Finalize VLine {}".format(self))


class VLine(ChartItem):

    def __init__(self, parent=None):
        super(VLine, self).__init__(parent)
        self._x = None
        self._label = None
        self._color = None
        self._bRect = None

        # self._flags = FLAG_NO_AUTO_RANGE | FLAG_NO_LABEL
        self.chartItemFlags = ChartItemFlags.FLAG_NO_AUTO_RANGE | ChartItemFlags.FLAG_NO_LABEL

    @property
    def color(self):
        return self._color

    @property
    def label(self):
        return self._label

    def setX(self, x, label=None, color=QColor(Qt.red)):
        self._x = x

        if label is not None:
            self._label = label

        self._color = color

        finfo = np.finfo(np.float32)

        self._bRect = QRectF(QPointF(x-1, finfo.max),
                             QPointF(x+1, finfo.min),)

    def boundingRect(self):
        """ Returns the bounding rect of the chart item
        :return: Bounding Rectangle
        :rtype: QRectF
        """
        return self._bRect

    def paint(self, p=QPainter(), o=QStyleOptionGraphicsItem(), widget=None):
        # _log.debug("LCI: paint")
        pen = makePen(self.color)
        p.setPen(pen)

        finfo = np.finfo(np.float32)

        self._path = QPainterPath()
        self._path.moveTo(self._x, finfo.max)
        self._path.lineTo(self._x, finfo.min)

        if self._path:
            p.drawPath(self._path)

        if DEBUG:
            p.setPen(Qt.yellow)
            p.drawRect(self._bRect)

    def __del__(self):
        _log.debug("Finalize VLine {}".format(self))