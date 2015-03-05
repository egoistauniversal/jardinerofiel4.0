from PyQt4 import QtGui, QtCore


class GroupDialog(QtGui.QDialog):
    def __init__(self, db, title, name='', parent=None):
        super(GroupDialog, self).__init__(parent)
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
        dialog = GroupDialog(db, title, name, parent)
        result = dialog.exec_()
        _nameStr = dialog._get_name()
        return _nameStr, result == QtGui.QDialog.Accepted

        # -----------------------------------------SECOND LEVEL CLOCK-----------------------------------------------


class ClockDialog(QtGui.QDialog):
    def __init__(self, db, title, group_id='', name='', time_on='', time_off='', pin='', parent=None):
        super(ClockDialog, self).__init__(parent)
        self._mainDB = db
        self._group_id = group_id
        self.setWindowTitle(title)
        # Nice widget for editing
        self._nameLabel = QtGui.QLabel('Nombre:', self)
        self._timeEditOnLabel = QtGui.QLabel('Encendido:', self)
        self._timeEditOffLabel = QtGui.QLabel('Apagado:', self)
        self._pinLabel = QtGui.QLabel('Pin:', self)

        self._nameLineEdit = QtGui.QLineEdit(self)
        self._timeEditOn = QtGui.QTimeEdit(self)
        self._timeEditOff = QtGui.QTimeEdit(self)
        self._pinComboBox = QtGui.QComboBox(self)

        # Used in order to check self._previousName vs new name
        self._previousName = name

        # OK and Cancel buttons
        self._dialogButtons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                                                     QtGui.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        self._setup(name, time_on, time_off, pin)

    def _setup(self, name, time_on, time_off, pin):
        self._timeEditOn.setDisplayFormat('HH:mm:ss')
        self._timeEditOff.setDisplayFormat('HH:mm:ss')

        self._setup_pin_combo_box(pin)

        if not QtCore.QString(name).isEmpty():
            self._nameLineEdit.setText(name)
            time = QtCore.QTime(int(time_on.mid(0, 2)), int(time_on.mid(3, 2)), int(time_on.mid(6, 2)))
            self._timeEditOn.setTime(time)
            time = QtCore.QTime(int(time_off.mid(0, 2)), int(time_off.mid(3, 2)), int(time_off.mid(6, 2)))
            self._timeEditOff.setTime(time)
            self._pinComboBox.setCurrentIndex(self._pinComboBox.findText(pin))

        self._layouts()
        self._connections()

    def _setup_pin_combo_box(self, pin):
        # Get list of pins available
        _allPinList = self._mainDB.pins_component_control_select_all()
        for _pin in _allPinList:
            self._pinComboBox.addItem(_pin)

        # Disable pins used
        _pinUsedList = self._mainDB.pins_component_control_table_select_pin_used(self._group_id)
        for item in _pinUsedList:
            if item != pin:
                # Get the index of the value to disable
                index = self._pinComboBox.model().index(self._pinComboBox.findText(item), 0)
                # This is the effective 'disable' flag
                v = QtCore.QVariant(0)
                # The Magic
                self._pinComboBox.model().setData(index, v, QtCore.Qt.UserRole - 1)

        # Select the next pin available
        for _pin in _allPinList:
            try:
                _pinUsedList.index(_pin)
            except ValueError:
                self._pinComboBox.setCurrentIndex(self._pinComboBox.findText(_pin))
                break

    def _layouts(self):
        _nameLayout = QtGui.QHBoxLayout()
        _nameLayout.addWidget(self._nameLabel)
        _nameLayout.addWidget(self._nameLineEdit)

        _timeEditOnLayout = QtGui.QHBoxLayout()
        _timeEditOnLayout.addWidget(self._timeEditOnLabel)
        _timeEditOnLayout.addWidget(self._timeEditOn)

        _timeEditOffLayout = QtGui.QHBoxLayout()
        _timeEditOffLayout.addWidget(self._timeEditOffLabel)
        _timeEditOffLayout.addWidget(self._timeEditOff)

        _pinLayout = QtGui.QHBoxLayout()
        _pinLayout.addWidget(self._pinLabel)
        _pinLayout.addWidget(self._pinComboBox)

        _mainLayout = QtGui.QVBoxLayout(self)
        _mainLayout.addLayout(_nameLayout)
        _mainLayout.addLayout(_timeEditOnLayout)
        _mainLayout.addLayout(_timeEditOffLayout)
        _mainLayout.addLayout(_pinLayout)
        _mainLayout.addWidget(self._dialogButtons)
        self.setLayout(_mainLayout)

    def _connections(self):
        self._dialogButtons.accepted.connect(self._validations)
        self._dialogButtons.rejected.connect(self.reject)

    def _validations(self):
        _validationIsOk = False
        if not self._nameLineEdit.text().isEmpty():
            self._nameLineEdit.setText(self._nameLineEdit.text().replace(' ', '_'))
            if self._timeEditOn.time() != self._timeEditOff.time():
                if self._nameLineEdit.text() == self._previousName:
                    _validationIsOk = True
                else:
                    if not self._mainDB.component_table_name_exist(str(self._group_id), str(self._nameLineEdit.text())):
                        _validationIsOk = True
                    else:
                        QtGui.QMessageBox().warning(self, 'Nombre ya existe', 'Nombre de componente ' +
                                                    self._nameLineEdit.text() + ' ya existe', QtGui.QMessageBox.Ok)
            else:
                QtGui.QMessageBox().warning(self, 'Tiempo Erroneo', 'La hora de encendido y apagado es el mismo',
                                            QtGui.QMessageBox.Ok)
                self._timeEditOn.setFocus()
        else:
            QtGui.QMessageBox().warning(self, 'Falta Nombre', 'No has escrito un nombre', QtGui.QMessageBox.Ok)
            self._nameLineEdit.setFocus()
        if _validationIsOk:
            self.accept()

    # Get data from dialog
    def _get_name(self):
        return str(self._nameLineEdit.text())

    def _get_time_on(self):
        _myTime = self._timeEditOn.time()
        return _myTime.toString("HH:mm:ss")

    def _get_time_off(self):
        _myTime = self._timeEditOff.time()
        return _myTime.toString("HH:mm:ss")

    def _get_pin(self):
        return self._pinComboBox.itemText(self._pinComboBox.currentIndex())

    # static method to create the dialog and return (name, time, etc, accepted)
    @staticmethod
    def get_data(db, title, group_id='', name='', time_on='', time_off='', pin='', parent=None):
        dialog = ClockDialog(db, title, group_id, name, time_on, time_off, pin, parent)
        result = dialog.exec_()
        _nameStr = dialog._get_name()
        _dateTimeOnStr = dialog._get_time_on()
        _dateTimeOffStr = dialog._get_time_off()
        _pinStr = dialog._get_pin()
        return _nameStr, _dateTimeOnStr, _dateTimeOffStr, _pinStr, result == QtGui.QDialog.Accepted

        # -----------------------------------------SECOND LEVEL TIMER-----------------------------------------------


class TimerDialog(QtGui.QDialog):
    def __init__(self, db, title, group_id='', name='', time_on='', time_off='', pin='', parent=None):
        super(TimerDialog, self).__init__(parent)
        self._mainDB = db
        self._group_id = group_id
        self.setWindowTitle(title)

        # Nice widget for editing
        self._nameLabel = QtGui.QLabel('Nombre:', self)
        self._timeEditOnLabel = QtGui.QLabel('Encendido:', self)
        self._timeEditOffLabel = QtGui.QLabel('Apagado:', self)
        self._pinLabel = QtGui.QLabel('Pin:', self)

        self._nameLineEdit = QtGui.QLineEdit(self)
        self._timeEditOn = QtGui.QTimeEdit(self)
        self._timeEditOff = QtGui.QTimeEdit(self)
        self._pinComboBox = QtGui.QComboBox(self)

        self._justLeaveItRadioButton = QtGui.QRadioButton('No hacer nada', self)
        self._resetOnRadioButton = QtGui.QRadioButton('Reiniciar en Encendido', self)
        self._resetOffRadioButton = QtGui.QRadioButton('Reiniciar en Apagado', self)
        self._resetRadioButtonGroup = QtGui.QGroupBox('Cuenta Atras', self)

        # Used in order to check self._previousName vs new name
        self._previousName = name

        # OK and Cancel buttons
        self._dialogButtons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                                                     QtGui.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        self._setup(name, time_on, time_off, pin)

    def _setup(self, name, time_on, time_off, pin):
        self._timeEditOn.setDisplayFormat('HH:mm:ss')
        self._timeEditOff.setDisplayFormat('HH:mm:ss')
        self._setup_pin_combo_box(pin)
        self._justLeaveItRadioButton.setChecked(True)
        self._set_style_sheet()

        if not QtCore.QString(name).isEmpty():
            self._nameLineEdit.setText(name)
            time = QtCore.QTime(int(time_on.mid(0, 2)), int(time_on.mid(3, 2)), int(time_on.mid(6, 2)))
            self._timeEditOn.setTime(time)
            time = QtCore.QTime(int(time_off.mid(0, 2)), int(time_off.mid(3, 2)), int(time_off.mid(6, 2)))
            self._timeEditOff.setTime(time)
            self._pinComboBox.setCurrentIndex(self._pinComboBox.findText(pin))

        self._layouts()
        self._connections()

    def _setup_pin_combo_box(self, pin):
        # Get list of pins available
        _allPinList = self._mainDB.pins_component_control_select_all()
        for _pin in _allPinList:
            self._pinComboBox.addItem(_pin)

        # Disable pins used
        _pinUsedList = self._mainDB.pins_component_control_table_select_pin_used(self._group_id)
        for item in _pinUsedList:
            if item != pin:
                # Get the index of the value to disable
                index = self._pinComboBox.model().index(self._pinComboBox.findText(item), 0)
                # This is the effective 'disable' flag
                v = QtCore.QVariant(0)
                # The Magic
                self._pinComboBox.model().setData(index, v, QtCore.Qt.UserRole - 1)

        # Select the next pin available
        for _pin in _allPinList:
            try:
                _pinUsedList.index(_pin)
            except ValueError:
                self._pinComboBox.setCurrentIndex(self._pinComboBox.findText(_pin))
                break

    def _layouts(self):
        _nameLayout = QtGui.QHBoxLayout()
        _nameLayout.addWidget(self._nameLabel)
        _nameLayout.addWidget(self._nameLineEdit)

        _timeEditOnLayout = QtGui.QHBoxLayout()
        _timeEditOnLayout.addWidget(self._timeEditOnLabel)
        _timeEditOnLayout.addWidget(self._timeEditOn)

        _timeEditOffLayout = QtGui.QHBoxLayout()
        _timeEditOffLayout.addWidget(self._timeEditOffLabel)
        _timeEditOffLayout.addWidget(self._timeEditOff)

        _pinLayout = QtGui.QHBoxLayout()
        _pinLayout.addWidget(self._pinLabel)
        _pinLayout.addWidget(self._pinComboBox)

        _resetRadioButtonGroupLayout = QtGui.QVBoxLayout()
        _resetRadioButtonGroupLayout.addWidget(self._justLeaveItRadioButton)
        _resetRadioButtonGroupLayout.addWidget(self._resetOnRadioButton)
        _resetRadioButtonGroupLayout.addWidget(self._resetOffRadioButton)
        self._resetRadioButtonGroup.setLayout(_resetRadioButtonGroupLayout)
        if self._nameLineEdit.text().isEmpty():
            self._resetRadioButtonGroup.setEnabled(False)

        _mainLayout = QtGui.QVBoxLayout(self)
        _mainLayout.addLayout(_nameLayout)
        _mainLayout.addLayout(_timeEditOnLayout)
        _mainLayout.addLayout(_timeEditOffLayout)
        _mainLayout.addLayout(_pinLayout)
        _mainLayout.addWidget(self._resetRadioButtonGroup)
        _mainLayout.addWidget(self._dialogButtons)
        self.setLayout(_mainLayout)

    def _connections(self):
        self._dialogButtons.accepted.connect(self._validations)
        self._dialogButtons.rejected.connect(self.reject)

    def _validations(self):
        _validationIsOk = False
        if not self._nameLineEdit.text().isEmpty():
            self._nameLineEdit.setText(self._nameLineEdit.text().replace(' ', '_'))
            _zeroTimeStr = QtCore.QTime(0, 0, 0, 0).toString("HH:mm:ss")
            _timeEditOnStr = self._timeEditOn.time().toString("HH:mm:ss")
            _timeEditOffStr = self._timeEditOff.time().toString("HH:mm:ss")
            if _timeEditOnStr != _zeroTimeStr and _timeEditOffStr != _zeroTimeStr:
                if self._nameLineEdit.text() == self._previousName:
                    _validationIsOk = True
                else:
                    if not self._mainDB.component_table_name_exist(str(self._group_id), str(self._nameLineEdit.text())):
                        _validationIsOk = True
                    else:
                        QtGui.QMessageBox().warning(self, 'Nombre ya existe', 'Nombre de componente ' +
                                                    self._nameLineEdit.text() + ' ya existe', QtGui.QMessageBox.Ok)
            else:
                QtGui.QMessageBox().warning(self, 'Tiempo Erroneo', 'No puede haber un tiempo de encendido o '
                                                                    'apagado de 00:00:00', QtGui.QMessageBox.Ok)
                self._timeEditOn.setFocus()
        else:
            QtGui.QMessageBox().warning(self, 'Falta Nombre', 'No has escrito un nombre', QtGui.QMessageBox.Ok)
            self._nameLineEdit.setFocus()
        if _validationIsOk:
            self.accept()

    # Get data from dialog
    def _get_name(self):
        return str(self._nameLineEdit.text())

    def _get_time_on(self):
        _myTime = self._timeEditOn.time()
        return _myTime.toString("HH:mm:ss")

    def _get_time_off(self):
        _myTime = self._timeEditOff.time()
        return _myTime.toString("HH:mm:ss")

    def _get_pin(self):
        return self._pinComboBox.itemText(self._pinComboBox.currentIndex())

    def _get_selected_reset_radio_button(self):
        _radio = None
        _buttonGroup = self._resetRadioButtonGroup.layout()
        for i in xrange(0, _buttonGroup.count()):
            widget = _buttonGroup.itemAt(i).widget()
            if widget.isChecked():
                _radio = i
                break
        return _radio

    def _reset_radio_button_group_is_enabled(self):
        return self._resetRadioButtonGroup.isEnabled()

    # static method to create the dialog and return (name, time, etc, accepted)
    @staticmethod
    def get_data(db, title, group_id='', name='', time_on='', time_off='', pin='', parent=None):
        dialog = TimerDialog(db, title, group_id, name, time_on, time_off, pin, parent)
        result = dialog.exec_()
        _nameStr = dialog._get_name()
        _timeOnStr = dialog._get_time_on()
        _timeOffStr = dialog._get_time_off()
        _pinStr = dialog._get_pin()
        if dialog._reset_radio_button_group_is_enabled():
            _radio_button = dialog._get_selected_reset_radio_button()
            return _nameStr, _timeOnStr, _timeOffStr, _pinStr, _radio_button, result == QtGui.QDialog.Accepted
        else:
            return _nameStr, _timeOnStr, _timeOffStr, _pinStr, result == QtGui.QDialog.Accepted

    def _set_style_sheet(self):
        self._resetRadioButtonGroup.setStyleSheet(
            'QGroupBox {border: 1px solid gray; border-radius: 5px; margin-top: 0.5em;}'
            'QGroupBox::title {subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px;}')


# ---------------------------------------SECOND LEVEL PULSAR-----------------------------------------------
class PulsarDialog(QtGui.QDialog):
    def __init__(self, db, title, group_id='', name='', time_on='', pin='', parent=None):
        super(PulsarDialog, self).__init__(parent)
        self._mainDB = db
        self._group_id = group_id
        self.setWindowTitle(title)

        # Nice widget for editing
        self._nameLabel = QtGui.QLabel('Nombre:', self)
        self._timeEditOnLabel = QtGui.QLabel('Encendido:', self)
        self._pinLabel = QtGui.QLabel('Pin:', self)

        self._nameLineEdit = QtGui.QLineEdit(self)
        self._timeEditOn = QtGui.QTimeEdit(self)
        self._pinComboBox = QtGui.QComboBox(self)

        self._justLeaveItRadioButton = QtGui.QRadioButton('No hacer nada', self)
        self._resetOnRadioButton = QtGui.QRadioButton('Reiniciar en Encendido', self)
        self._resetRadioButtonGroup = QtGui.QGroupBox('Cuenta Atras', self)

        # Used in order to check self._previousName vs new name
        self._previousName = name

        # OK and Cancel buttons
        self._dialogButtons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                                                     QtGui.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        self._setup(name, time_on, pin)

    def _setup(self, name, time_on, pin):
        self._timeEditOn.setDisplayFormat('HH:mm:ss')
        self._setup_pin_combo_box(pin)
        self._justLeaveItRadioButton.setChecked(True)
        self._set_style_sheet()

        if not QtCore.QString(name).isEmpty():
            self._nameLineEdit.setText(name)
            time = QtCore.QTime(int(time_on.mid(0, 2)), int(time_on.mid(3, 2)), int(time_on.mid(6, 2)))
            self._timeEditOn.setTime(time)
            self._pinComboBox.setCurrentIndex(self._pinComboBox.findText(pin))

        self._layouts()
        self._connections()

    def _setup_pin_combo_box(self, pin):
        # Get list of pins available
        _allPinList = self._mainDB.pins_component_control_select_all()
        for _pin in _allPinList:
            self._pinComboBox.addItem(_pin)

        # Disable pins used
        _pinUsedList = self._mainDB.pins_component_control_table_select_pin_used(self._group_id)
        for item in _pinUsedList:
            if item != pin:
                # Get the index of the value to disable
                index = self._pinComboBox.model().index(self._pinComboBox.findText(item), 0)
                # This is the effective 'disable' flag
                v = QtCore.QVariant(0)
                # The Magic
                self._pinComboBox.model().setData(index, v, QtCore.Qt.UserRole - 1)

        # Select the next pin available
        for _pin in _allPinList:
            try:
                _pinUsedList.index(_pin)
            except ValueError:
                self._pinComboBox.setCurrentIndex(self._pinComboBox.findText(_pin))
                break

    def _layouts(self):
        _nameLayout = QtGui.QHBoxLayout()
        _nameLayout.addWidget(self._nameLabel)
        _nameLayout.addWidget(self._nameLineEdit)

        _timeEditOnLayout = QtGui.QHBoxLayout()
        _timeEditOnLayout.addWidget(self._timeEditOnLabel)
        _timeEditOnLayout.addWidget(self._timeEditOn)

        _pinLayout = QtGui.QHBoxLayout()
        _pinLayout.addWidget(self._pinLabel)
        _pinLayout.addWidget(self._pinComboBox)

        _resetRadioButtonGroupLayout = QtGui.QVBoxLayout()
        _resetRadioButtonGroupLayout.addWidget(self._justLeaveItRadioButton)
        _resetRadioButtonGroupLayout.addWidget(self._resetOnRadioButton)
        self._resetRadioButtonGroup.setLayout(_resetRadioButtonGroupLayout)
        if self._nameLineEdit.text().isEmpty():
            self._resetRadioButtonGroup.setEnabled(False)

        _mainLayout = QtGui.QVBoxLayout(self)
        _mainLayout.addLayout(_nameLayout)
        _mainLayout.addLayout(_timeEditOnLayout)
        _mainLayout.addLayout(_pinLayout)
        _mainLayout.addWidget(self._resetRadioButtonGroup)
        _mainLayout.addWidget(self._dialogButtons)
        self.setLayout(_mainLayout)

    def _connections(self):
        self._dialogButtons.accepted.connect(self._validations)
        self._dialogButtons.rejected.connect(self.reject)

    def _validations(self):
        _validationIsOk = False
        if not self._nameLineEdit.text().isEmpty():
            self._nameLineEdit.setText(self._nameLineEdit.text().replace(' ', '_'))
            _zeroTimeStr = QtCore.QTime(0, 0, 0, 0).toString("HH:mm:ss")
            _timeEditOnStr = self._timeEditOn.time().toString("HH:mm:ss")
            if _timeEditOnStr != _zeroTimeStr:
                if self._nameLineEdit.text() == self._previousName:
                    _validationIsOk = True
                else:
                    if not self._mainDB.component_table_name_exist(str(self._group_id), str(self._nameLineEdit.text())):
                        _validationIsOk = True
                    else:
                        QtGui.QMessageBox().warning(self, 'Nombre ya existe', 'Nombre de componente ' +
                                                    self._nameLineEdit.text() + ' ya existe', QtGui.QMessageBox.Ok)
            else:
                QtGui.QMessageBox().warning(self, 'Tiempo Erroneo', 'No puede haber un tiempo de encendido de 00:00:00',
                                            QtGui.QMessageBox.Ok)
                self._timeEditOn.setFocus()
        else:
            QtGui.QMessageBox().warning(self, 'Falta Nombre', 'No has escrito un nombre', QtGui.QMessageBox.Ok)
            self._nameLineEdit.setFocus()
        if _validationIsOk:
            self.accept()

    # Get data from dialog
    def _get_name(self):
        return str(self._nameLineEdit.text())

    def _get_time_on(self):
        _myTime = self._timeEditOn.time()
        return _myTime.toString("HH:mm:ss")

    def _get_pin(self):
        return self._pinComboBox.itemText(self._pinComboBox.currentIndex())

    def _get_selected_reset_radio_button(self):
        _radio = None
        _buttonGroup = self._resetRadioButtonGroup.layout()
        for i in xrange(0, _buttonGroup.count()):
            widget = _buttonGroup.itemAt(i).widget()
            if widget.isChecked():
                _radio = i
                break
        return _radio

    def _reset_radio_button_group_is_enabled(self):
        return self._resetRadioButtonGroup.isEnabled()

    # static method to create the dialog and return (name, time, etc, accepted)
    @staticmethod
    def get_data(db, title, group_id='', name='', time_on='', pin='', parent=None):
        dialog = PulsarDialog(db, title, group_id, name, time_on, pin, parent)
        result = dialog.exec_()
        _nameStr = dialog._get_name()
        _timeOnStr = dialog._get_time_on()
        _pinStr = dialog._get_pin()
        if dialog._reset_radio_button_group_is_enabled():
            _radio_button = dialog._get_selected_reset_radio_button()
            return _nameStr, _timeOnStr, _pinStr, _radio_button, result == QtGui.QDialog.Accepted
        else:
            return _nameStr, _timeOnStr, _pinStr, result == QtGui.QDialog.Accepted

    def _set_style_sheet(self):
        self._resetRadioButtonGroup.setStyleSheet(
            'QGroupBox {border: 1px solid gray; border-radius: 5px; margin-top: 0.5em;}'
            'QGroupBox::title {subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px;}')