from PySide2 import QtCore, QtWidgets, QtGui


class SGraphicsView(QtWidgets.QGraphicsView):

    # Constant settings
    EDGE_DRAG_START_THRESHOLD = 50
    HIGH_QUALITY_ZOOM = 4

    def __init__(self, gr_scene, parent=None):
        super().__init__(parent)

        self.gr_scene = gr_scene
        self.zoom_in_factor = 1.25
        self.zoom_clamp = True
        self.zoom = 10
        self.zoom_step = 1
        self.zoom_range = (-5.0, 15.0)

        self.init_ui()
        self.setScene(self.gr_scene)

    def init_ui(self):
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        # 关闭卷栏
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        # 开启拖放
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.setAcceptDrops(True)

    def update_render_hints(self):
        if self.zoom > self.HIGH_QUALITY_ZOOM:
            self.setRenderHints(
                QtGui.QPainter.Antialiasing
                | QtGui.QPainter.HighQualityAntialiasing
                | QtGui.QPainter.TextAntialiasing
                | QtGui.QPainter.SmoothPixmapTransform
            )
        else:
            self.setRenderHints(
                QtGui.QPainter.Antialiasing | QtGui.QPainter.TextAntialiasing | QtGui.QPainter.SmoothPixmapTransform
            )
    # =========== Qt Events overrides =========== #

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
            self.middle_mouse_press(event)
        elif event.button() == QtCore.Qt.LeftButton:
            self.left_mouse_press(event)
        elif event.button() == QtCore.Qt.RightButton:
            self.right_mouse_press(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
            self.middle_mouse_release(event)
        elif event.button() == QtCore.Qt.LeftButton:
            self.left_mouse_release(event)
        elif event.button() == QtCore.Qt.RightButton:
            self.right_mouse_release(event)
        else:
            super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        zoom_out_factor = 1.0 / self.zoom_in_factor

        if event.angleDelta().y() > 0:
            zoom_factor = self.zoom_in_factor
            self.zoom += self.zoom_step
        else:
            zoom_factor = zoom_out_factor
            self.zoom -= self.zoom_step

        clamped = False
        if self.zoom < self.zoom_range[0]:
            self.zoom, clamped = self.zoom_range[0], True
        if self.zoom > self.zoom_range[1]:
            self.zoom, clamped = self.zoom_range[1], True

        # Set actual scale
        if not clamped or not self.zoom_clamp:
            self.scale(zoom_factor, zoom_factor)
            self.update_render_hints()

    def left_mouse_press(self, event):
        super().mousePressEvent(event)

    def left_mouse_release(self, event):
        super().mouseReleaseEvent(event)

    def middle_mouse_press(self, event):
        releaseEvent = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonRelease,
            event.localPos(),
            event.screenPos(),
            QtCore.Qt.LeftButton,
            QtCore.Qt.NoButton,
            event.modifiers(),
        )
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.setInteractive(False)
        fake_event = QtGui.QMouseEvent(
            event.type(),
            event.localPos(),
            event.screenPos(),
            QtCore.Qt.LeftButton,
            event.buttons() | QtCore.Qt.LeftButton,
            event.modifiers(),
        )
        super().mousePressEvent(fake_event)

    def middle_mouse_release(self, event):
        fake_event = QtGui.QMouseEvent(
            event.type(),
            event.localPos(),
            event.screenPos(),
            QtCore.Qt.LeftButton,
            event.buttons() & ~QtCore.Qt.LeftButton,
            event.modifiers(),
        )
        super().mouseReleaseEvent(fake_event)
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.setInteractive(True)

    def right_mouse_press(self, event):
        super().mousePressEvent(event)

    def right_mouse_release(self, event):
        super().mouseReleaseEvent(event)
