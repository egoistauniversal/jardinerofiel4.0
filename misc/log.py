from PyQt4 import QtGui, QtCore


class Log(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        # find user home directory
        self._directory = QtCore.QDir(QtCore.QDir().home().path() + '/jf/log')
        # Create directory if it doesn't exist
        if not self._directory.exists():
            QtCore.QDir().mkpath(self._directory.path())
        self._previousDate = QtCore.QDate().currentDate()
        self._file = QtCore.QFile(self._directory.path() + '/' +
                                  self._previousDate.toString('yyyy-MM-dd') + '_log.txt')

    def write(self, output):
        _currentDate = QtCore.QDate().currentDate()
        if _currentDate.getDate() != self._previousDate.getDate():
            self._file.close()
            self._previousDate.setDate(_currentDate.year(), _currentDate.month(), _currentDate.day())
            # TODO checkear si funciona la creacion del nuevo fichero mientras corre el programa
            # self._file = QtCore.QFile(self._directory.path() + '/' +
            #                           self._previousDate.toString('yyyy-MM-dd') + '_log.txt')

        if not self._file.open(QtCore.QIODevice.Append | QtCore.QFile.Text):
            QtGui.QMessageBox().warning(self, 'Fichero', 'No se puede crear el fichero %s:\n%s' %
                                        (self._file.fileName(), self._file.errorString()))
        else:
            _stream = QtCore.QTextStream(self._file)
            _stream << output + '\n'
            self._file.close()