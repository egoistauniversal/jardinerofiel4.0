from PyQt4 import QtGui, QtCore


class GroupDialog(QtGui.QDialog):
    def __init__(self, db, title, radio, name, parent):
        super(GroupDialog, self).__init__(parent)
        self._mainDB = db
        self.setWindowTitle(title)
        # Nice widget for editing
        self._nameLabel = QtGui.QLabel('Nombre:', self)
        self._radioLabel = QtGui.QLabel('Radio:', self)

        self._nameLineEdit = QtGui.QLineEdit(self)
        self._radioComboBox = QtGui.QComboBox(self)

        self._previousName = name

        # OK and Cancel buttons
        self._dialogButtons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                                                     QtGui.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        self._setup(radio, name)

    def _setup(self, radio, name):
        self._setup_radio_combobox(radio)
        if name:
            self._nameLineEdit.setText(name)
            self._radioComboBox.setCurrentIndex(self._radioComboBox.findData(radio))
        self._layouts()
        self._connections()

    def _setup_radio_combobox(self, radio):
        _radioList = [1, 2, 3, 4]
        for _radio in _radioList:
            self._radioComboBox.addItem(str(_radio), _radio)

        # Disable radio in use
        _radioUsedList = self._mainDB.group_node_table_select_radio()
        for item in _radioUsedList:
            if item != radio:
                # Get the index of the value to disable
                index = self._radioComboBox.model().index(self._radioComboBox.findData(item), 0)
                # This is the effective 'disable' flag
                v = QtCore.QVariant(0)
                # The Magic
                self._radioComboBox.model().setData(index, v, QtCore.Qt.UserRole - 1)

        # Select the next pin available
        for _radio in _radioList:
            try:
                _radioUsedList.index(_radio)
            except ValueError:
                self._radioComboBox.setCurrentIndex(self._radioComboBox.findData(_radio))
                break

    def _layouts(self):
        _nameLayout = QtGui.QHBoxLayout()
        _nameLayout.addWidget(self._nameLabel)
        _nameLayout.addWidget(self._nameLineEdit)

        _radioLayout = QtGui.QHBoxLayout()
        _radioLayout.addWidget(self._radioLabel)
        _radioLayout.addWidget(self._radioComboBox)

        _mainLayout = QtGui.QVBoxLayout(self)
        _mainLayout.addLayout(_nameLayout)
        _mainLayout.addLayout(_radioLayout)
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

    def _get_radio(self):
        return self._radioComboBox.itemData(self._radioComboBox.currentIndex()).toInt()[0]

    # static method to create the dialog and return (name, time, etc, accepted)
    @staticmethod
    def get_data(db, title, radio=0, name='', parent=None):
        dialog = GroupDialog(db, title, radio, name, parent)
        result = dialog.exec_()
        _nameStr = dialog._get_name()
        _radio = dialog._get_radio()
        return _radio, _nameStr, result == QtGui.QDialog.Accepted