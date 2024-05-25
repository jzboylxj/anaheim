import sys
from PySide2 import QtCore, QtGui, QtWidgets

try:
    sys.path.append("D:\\Works\\studio\\maya_pipeline\\anaheim")
except Exception:
    pass

from suit_creator.widgets.node_editor import NodeEditor


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    node_editor = NodeEditor()
    node_editor.show()

    sys.exit(app.exec_())
