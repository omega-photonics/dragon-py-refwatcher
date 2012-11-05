from PyQt4 import QtCore
import shelve

class Model(QtCore.QObject):
    changed = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent=parent)
        self.storage = shelve.open("settings")
        try:
            self.bits = self.storage['bits']
        except KeyError:
            self.bits = 8
            self.storage['bits'] = 8

    def set_bits(self, value):
        self.bits = value
        self.storage['bits'] = value
        self.changed.emit()

if __name__ == '__main__':
    from PyQt4 import QtGui
    import sys

    app = QtGui.QApplication(sys.argv)
    model = Model()
    wnd = QtGui.QPushButton(str(model.bits))
    wnd.clicked.connect(lambda: model.set_bits(8 if model.bits == 12 else 12))
    model.changed.connect(lambda: wnd.setText(str(model.bits)))
    wnd.show()
    sys.exit(app.exec_())
