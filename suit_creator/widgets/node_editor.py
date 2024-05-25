from PySide2 import QtCore, QtWidgets, QtGui


from suit_creator.widgets import graphics_view, node_scene


class NodeEditor(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setMinimumSize(200, 500)

        self.init_layout()

    def init_layout(self):
        self.scene = node_scene.Scene()

        self.view = graphics_view.SGraphicsView(self.scene.gr_scene, self)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.view)
