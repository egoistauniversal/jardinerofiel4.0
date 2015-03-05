from PyQt4 import QtGui, QtCore


class MessageBox(QtCore.QObject):
    @staticmethod
    def close_app(parent):
        reply = QtGui.QMessageBox().question(parent, 'Cerrar', 'Estas seguro que quieres cerrar el programa?',
                                             QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        return reply