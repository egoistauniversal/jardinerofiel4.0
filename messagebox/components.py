from PyQt4 import QtGui, QtCore


class MessageBox(QtCore.QObject):
    @staticmethod
    def activate_component(parent, name):
        _reply = QtGui.QMessageBox().question(parent, 'Activar',
                                              'Estas seguro que quieres ACTIVAR la PROGRAMACION del componente '
                                              + name + '?',
                                              QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        return _reply

    @staticmethod
    def deactivate_component(parent, name):
        _reply = QtGui.QMessageBox().question(parent, 'Desactivar',
                                              'Estas seguro que quieres DESACTIVAR la PROGRAMACION del componente '
                                              + name + '?',
                                              QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        return _reply

    @staticmethod
    def remove_component(parent, name):
        _reply = QtGui.QMessageBox().question(parent, 'Eliminar',
                                              'Estas seguro que quieres ELIMINAR el componente ' + name + '?',
                                              QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        return _reply

    @staticmethod
    def remove_group(parent, name):
        _reply = QtGui.QMessageBox().question(parent, 'Eliminar',
                                              'Estas seguro que quieres ELIMINAR el grupo ' + name +
                                              ' con todos sus componentes sensores, controles, etc, etc?',
                                              QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        return _reply