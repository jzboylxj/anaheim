import itertools
import math
from PySide2 import QtCore, QtGui, QtWidgets


class SGraphicsScene(QtWidgets.QGraphicsScene):

    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.scene = scene

        # Settings
        self.grid_size = 50
        # Colors
        self._color_background = QtGui.QColor("#222933")
        self._color_point = QtGui.QColor("#d3d4d6")

        self.setBackgroundBrush(self._color_background)

    # ======== Events ========= #

    def dragMoveEvent(self, event):
        # Disable parent event
        pass

    # ======== Methods ========= #

    def set_scene_size(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)

        painter.setPen(self._color_point)
        for x, y in itertools.product(
            range(first_left, right, self.grid_size),
            range(first_top, bottom, self.grid_size),
        ):
            painter.drawPoint(x, y)
