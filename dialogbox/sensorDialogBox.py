from PyQt4 import QtGui, QtCore


class FirstLevelItemDialog(QtGui.QDialog):
    def __init__(self, db,  title, name='', parent=None):
        super(FirstLevelItemDialog, self).__init__(parent)
        self._mainDB = db
        self.setWindowTitle(title)
        # Nice widget for editing
        self._nameLabel = QtGui.QLabel('Nombre:', self)
        self._nameLineEdit = QtGui.QLineEdit(self)
        self._previousName = name

        # OK and Cancel buttons
        self._dialogButtons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                                                     QtGui.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        self._setup()

    def _setup(self):
        self._nameLineEdit.setText(self._previousName)
        self._layouts()
        self._connections()

    def _layouts(self):
        _nameLayout = QtGui.QHBoxLayout()
        _nameLayout.addWidget(self._nameLabel)
        _nameLayout.addWidget(self._nameLineEdit)

        _mainLayout = QtGui.QVBoxLayout(self)
        _mainLayout.addLayout(_nameLayout)
        _mainLayout.addWidget(self._dialogButtons)
        self.setLayout(_mainLayout)

    def _connections(self):
        self._dialogButtons.accepted.connect(self._validations)
        self._dialogButtons.rejected.connect(self.reject)

    def _validations(self):
        if self._nameLineEdit.text().isEmpty():
            QtGui.QMessageBox().warning(self, 'Falta Nombre', 'No has escrito un nombre', QtGui.QMessageBox.Ok)
            self._nameLineEdit.setFocus()
        else:
            self._nameLineEdit.setText(self._nameLineEdit.text().replace(' ', '_'))
            if self._nameLineEdit.text() == self._previousName:
                self.accept()
            else:
                if not self._mainDB.group_node_table_name_exist(str(self._nameLineEdit.text())):
                    self.accept()
                else:
                    QtGui.QMessageBox().warning(self, 'Nombre ya existe', 'Nombre de grupo ' +
                                                self._nameLineEdit.text() + ' ya existe', QtGui.QMessageBox.Ok)

        # Get data from dialog
    def _get_name(self):
        return self._nameLineEdit.text()

    # static method to create the dialog and return (name, time, etc, accepted)
    @staticmethod
    def get_data(db, title, name='', parent=None):
        dialog = FirstLevelItemDialog(db, title, name, parent)
        result = dialog.exec_()
        _nameStr = dialog._get_name()
        return _nameStr, result == QtGui.QDialog.Accepted