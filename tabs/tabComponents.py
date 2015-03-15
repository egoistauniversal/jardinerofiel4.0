from PyQt4 import QtGui, QtCore
from dialogbox import componentDialogBox, groupDialogBox
from misc import treeView, contextMenu
from actions import groupActions, componentActions
from messagebox import components


class TabComponents(QtGui.QWidget):
    insertGroupSignal = QtCore.pyqtSignal(int, int, str)
    modifyGroupSignal = QtCore.pyqtSignal(QtCore.QModelIndex, str)
    removeGroupSignal = QtCore.pyqtSignal(QtCore.QModelIndex, int)

    def __init__(self, db, serial, browser):
        super(TabComponents, self).__init__()
        self._model = QtGui.QStandardItemModel(0, 8, self)
        self._mainDB = db
        self._serial = serial
        self._browser = browser
        self._myTreeView = treeView.TreeView()
        self._actions = componentActions.ComponentActions()
        self._setup()

    def _setup(self):
        self._setup_model()
        self._setup_layouts()
        self._setup_connections()
        self._mainDB.read_component_structure(self._model, self._serial)

    def _setup_model(self):
        self._model.setHeaderData(0, QtCore.Qt.Horizontal, 'Nombre')
        self._model.setHeaderData(1, QtCore.Qt.Horizontal, 'Tipo')
        self._model.setHeaderData(2, QtCore.Qt.Horizontal, 'Encendido')
        self._model.setHeaderData(3, QtCore.Qt.Horizontal, 'Apagado')
        self._model.setHeaderData(4, QtCore.Qt.Horizontal, 'Restante')
        self._model.setHeaderData(5, QtCore.Qt.Horizontal, 'Estado')
        self._model.setHeaderData(6, QtCore.Qt.Horizontal, 'Pin')
        self._model.setHeaderData(7, QtCore.Qt.Horizontal, 'Programado')
        self._model.appendRow(QtGui.QStandardItem('Componentes'))
        self._myTreeView.setModel(self._model)

    def _setup_layouts(self):
        _treeViewLayout = QtGui.QHBoxLayout()
        _treeViewLayout.addWidget(self._myTreeView)
        self.setLayout(_treeViewLayout)

    def _setup_connections(self):
        self._myTreeView.customContextMenuRequested.connect(self._open_context_menu)

    # -------------------------------------------GROUP_NODE--------------------------------------------------------

    def _signal_add_group_node(self):
        # Get data from Dialog box
        _radio, _name, _ok = groupDialogBox.GroupDialog.get_data(self._mainDB, 'Anadir Grupo')
        if _ok:
            _id = self._mainDB.group_node_table_insert_row(_radio, str(_name))
            self.insertGroupSignal.emit(_id, _radio, _name)

    def _signal_modify_group_node(self, index):
        # Get data from Dialog box
        _previousGroupName = index.model().itemFromIndex(index).get_name()
        _previousRadio = index.model().itemFromIndex(index).get_radio()
        _radio, _newGroupName, _ok = groupDialogBox.GroupDialog.get_data(self._mainDB,
                                                                         'Modificar Grupo ' + _previousGroupName,
                                                                         radio=_previousRadio,
                                                                         name=_previousGroupName)
        if _ok:
            _group_id = index.model().itemFromIndex(index).get_id()
            self._mainDB.group_node_table_modify_row(_group_id, _radio, str(_newGroupName))
            self.modifyGroupSignal.emit(index, _newGroupName)

    def _signal_remove_group_node(self, index):
        # Structure of _list = [_id, _name]
        _list = self._actions.get_remove_data(index)
        _reply = components.MessageBox.remove_group(self, _list[1])
        if _reply == QtGui.QMessageBox.Yes:
            self.removeGroupSignal.emit(index, _list[0])

    def add_group_node(self, group_id, group_radio, group_name):
        groupActions.GroupActions().add(self._model, group_id, group_radio, group_name)

    def modify_group_node(self, index, group_radio, group_name):
        groupActions.GroupActions().modify(self._model, index, group_radio, group_name)

    def remove_group_node(self, index, group_id):
        self._actions.remove_item_from_group(index)
        groupActions.GroupActions().remove(self._model, index)
        self._mainDB.component_table_remove_row_by_group_id(group_id)
        self._mainDB.group_node_table_remove_row(group_id)

    # -------------------------------------------ADD--------------------------------------------------------

    def _add_clock_node(self, index):
        # Get group_id from index
        _group_id = index.model().itemFromIndex(index).get_id()
        # Get data from Dialog box
        _name, _timeOn, _timeOff, _pin, ok = \
            componentDialogBox.ClockDialog.get_data(self._mainDB, 'Anadir Reloj', group_id=_group_id)
        if ok:
            _timeType = 1
            _id = self._mainDB.component_table_insert_row(_group_id, str(_name), _timeType, str(_timeOn),
                                                          str(_timeOff), _pin, True)
            self._actions.add_clock_node(index, _id, _name, _timeType, _timeOn, _timeOff, _pin, True, self._serial)

    def _add_timer_node(self, index):
        # Get group_id from index
        _group_id = index.model().itemFromIndex(index).get_id()
        # Get data from Dialog box
        _name, _timeOn, _timeOff, _pin, _ok = \
            componentDialogBox.TimerDialog.get_data(self._mainDB, 'Anadir Temporizador', group_id=_group_id)
        if _ok:
            _timeType = 2
            _id = self._mainDB.component_table_insert_row(_group_id, str(_name), _timeType, str(_timeOn),
                                                          str(_timeOff), str(_pin), True)
            self._actions.add_timer_node(index, _id, _name, _timeType, _timeOn, _timeOff, _pin, True, self._serial)

    def _add_pulsar_node(self, index):
        # Get group_id from index
        _group_id = index.model().itemFromIndex(index).get_id()
        # Get data from Dialog box
        _name, _timeOn, _pin, _ok = componentDialogBox.PulsarDialog.get_data(self._mainDB, 'Anadir Pulsador',
                                                                             group_id=_group_id)
        if _ok:
            _timeType = 3
            _id = self._mainDB.component_table_insert_row(_group_id, str(_name), _timeType, str(_timeOn), str(''),
                                                          str(_pin), True)
            self._actions.add_pulsar_node(index, _id, _name, _timeType, _timeOn, _pin, True, self._serial)

    # -------------------------------------------MODIFY--------------------------------------------------------

    def _modify_second_level_node(self, index):
        _componentType = self._actions.get_type(index)
        if _componentType == 1:
            # Structure of _list = [_group_id, _id, _name, _timeType, _timeOn, _timeOff, _pin]
            _list = self._actions.get_row_data(index)
            _name, _timeOn, _timeOff, _pin, _ok = \
                componentDialogBox.ClockDialog.get_data(self._mainDB, 'Modificar Reloj', group_id=_list[0],
                                                        name=_list[2], time_on=_list[4], time_off=_list[5],
                                                        pin=_list[6])
            if _ok:
                self._mainDB.component_table_modify_row(_list[1], str(_name), str(_timeOn), str(_timeOff), str(_pin))
                self._actions.modify_clock_node(index, _name, _timeOn, _timeOff, _pin)

        elif _componentType == 2:
            # Structure of _list = [_group_id, _id, _name, _timeType, _timeOn, _timeOff, _pin]
            _list = self._actions.get_row_data(index)
            _name, _timeOn, _timeOff, _pin, _reset, _ok = \
                componentDialogBox.TimerDialog.get_data(self._mainDB, 'Modificar Temporizador', group_id=_list[0],
                                                        name=_list[2], time_on=_list[4], time_off=_list[5],
                                                        pin=_list[6])
            if _ok:
                self._mainDB.component_table_modify_row(_list[1], str(_name), str(_timeOn), str(_timeOff), str(_pin))
                self._actions.modify_timer_node(index, _name, _timeOn, _timeOff, _pin, _reset)

        if _componentType == 3:
            # Structure of _list = [_group_id, _id, _name, _timeType, _timeOn, _pin]
            _list = self._actions.get_pulsar_row_data(index)
            _name, _timeOn, _pin, _reset, _ok = componentDialogBox.PulsarDialog.get_data(self._mainDB,
                                                                                         'Anadir Pulsador',
                                                                                         group_id=_list[0],
                                                                                         name=_list[2],
                                                                                         time_on=_list[4], pin=_list[5])
            if _ok:
                self._mainDB.component_table_modify_row(_list[1], str(_name), str(_timeOn), str(''), str(_pin))
                self._actions.modify_pulsar_node(index, _name, _timeOn, _pin, _reset)

    # -------------------------------------------REMOVE--------------------------------------------------------

    def _remove_second_level_node(self, index):
        # Structure _list = [_id, _name]
        _list = self._actions.get_remove_data(index)
        _reply = components.MessageBox().remove_component(self, _list[1])
        if _reply == QtGui.QMessageBox.Yes:
            self._actions.remove_second_level_node(index)
            self._mainDB.component_table_remove_row_by_id(_list[0])

    # -------------------------------------------ACTIVATE-DEACTIVATE--------------------------------------------------

    def _activate_deactivate_second_level_node(self, index):
        # Structure of _list = [_id, _name, _active]
        _list = self._actions.get_active_data(index)
        # if component is active
        if _list[2]:
            _reply = components.MessageBox().deactivate_component(self, _list[1])
            if _reply == QtGui.QMessageBox.Yes:
                # Deactivate component
                self._mainDB.component_table_modify_column_active(_list[0], False)
                self._actions.set_active(index, False)
        else:
            _reply = components.MessageBox().activate_component(self, _list[1])
            if _reply == QtGui.QMessageBox.Yes:
                # Activate component
                self._mainDB.component_table_modify_column_active(_list[0], True)
                self._actions.set_active(index, True)

    # ---------------------------------------CONTEXT MENU---------------------------------------------

    def _open_context_menu(self, point):
        _currentIndex = self._myTreeView.indexAt(point)
        # if it's been clicked on any element from the state AND if the item has parent then...
        if _currentIndex.isValid():
            # Get item's level
            level = self._get_item_level(_currentIndex)
            if level == 0:
                self._show_root_context_menu(point)
            elif level == 1:
                self._show_first_level_context_menu(point, _currentIndex)
            elif level == 2:
                self._show_second_level_context_menu(point, _currentIndex)

    def _show_root_context_menu(self, point):
        _mainContextMenu = QtGui.QMenu()
        _mainContextMenu.addAction('Anadir Grupo', self._signal_add_group_node)
        _mainContextMenu.exec_(self.mapToGlobal(point))

    def _show_first_level_context_menu(self, point, index):
        _contextMenu = contextMenu.Options()
        _subMenuAnadir = QtGui.QMenu()
        _subMenuAnadir.setTitle('Anadir')
        _subMenuAnadir.addAction(_contextMenu.get_component_name(1),
                                 lambda: self._add_clock_node(index))
        _subMenuAnadir.addAction(_contextMenu.get_component_name(2),
                                 lambda: self._add_timer_node(index))
        _subMenuAnadir.addAction(_contextMenu.get_component_name(3),
                                 lambda: self._add_pulsar_node(index))

        _mainContextMenu = QtGui.QMenu()
        _mainContextMenu.addMenu(_subMenuAnadir)
        _mainContextMenu.addAction('Modificar', lambda: self._signal_modify_group_node(index))
        _mainContextMenu.addAction('Eliminar', lambda: self._signal_remove_group_node(index))
        _mainContextMenu.exec_(self.mapToGlobal(point))

    def _show_second_level_context_menu(self, point, index):
        _componentType = self._actions.get_type(index)
        if _componentType == 1:
            self._clock_context_menu(point, index)
        elif _componentType == 2:
            self._timer_context_menu(point, index)
        elif _componentType == 3:
            self._pulsar_context_menu(point, index)

    def _clock_context_menu(self, point, index):
        _mainContextMenu = QtGui.QMenu()
        _mainContextMenu.addAction('Modificar', lambda: self._modify_second_level_node(index))
        _mainContextMenu.addAction('Eliminar', lambda: self._remove_second_level_node(index))
        _mainContextMenu.addSeparator()
        if self._actions.is_active(index):
            _mainContextMenu.addAction('Desactivar Programacion',
                                       lambda: self._activate_deactivate_second_level_node(index))
            _mainContextMenu.addSeparator()
            if self._actions.timer_is_active(index):
                _mainContextMenu.addAction('Pausar cuenta atras',
                                           lambda: self._actions.pause_timer(index))
            else:
                _mainContextMenu.addAction('Reanudar cuenta atras',
                                           lambda: self._actions.start_timer(index))
                _mainContextMenu.addSeparator()
                if self._actions.state_is_on(index):
                    _mainContextMenu.addAction('Apagado Manual',
                                               lambda: self._actions.set_state(index, False))
                else:
                    _mainContextMenu.addAction('Encendido Manual',
                                               lambda: self._actions.set_state(index, True))
        else:
            _mainContextMenu.addAction('Activar Programacion',
                                       lambda: self._activate_deactivate_second_level_node(index))

        _mainContextMenu.exec_(self.mapToGlobal(point))

    def _timer_context_menu(self, point, index):
        _mainContextMenu = QtGui.QMenu()
        _mainContextMenu.addAction('Modificar', lambda: self._modify_second_level_node(index))
        _mainContextMenu.addAction('Eliminar', lambda: self._remove_second_level_node(index))
        _mainContextMenu.addSeparator()
        if self._actions.is_active(index):
            _mainContextMenu.addAction('Desactivar Programacion',
                                       lambda: self._activate_deactivate_second_level_node(index))
            _mainContextMenu.addSeparator()
            if self._actions.timer_is_active(index):
                _mainContextMenu.addAction('Pausar cuenta atras',
                                           lambda: self._actions.pause_timer(index))
            else:
                _mainContextMenu.addAction('Reanudar cuenta atras',
                                           lambda: self._actions.start_timer(index))
                _mainContextMenu.addAction('Reanudar cuenta atras en Encendido',
                                           lambda: self._actions.resume_countdown_with_time_on(index))
                _mainContextMenu.addAction('Reanudar cuenta atras en Apagado',
                                           lambda: self._actions.resume_countdown_with_time_off(index))
                _mainContextMenu.addSeparator()
                if self._actions.state_is_on(index):
                    _mainContextMenu.addAction('Apagado Manual',
                                               lambda: self._actions.set_state(index, False))
                else:
                    _mainContextMenu.addAction('Encendido Manual',
                                               lambda: self._actions.set_state(index, True))
        else:
            _mainContextMenu.addAction('Activar Programacion',
                                       lambda: self._activate_deactivate_second_level_node(index))
        _mainContextMenu.exec_(self.mapToGlobal(point))

    def _pulsar_context_menu(self, point, index):
        _mainContextMenu = QtGui.QMenu()
        _mainContextMenu.addAction('Modificar', lambda: self._modify_second_level_node(index))
        _mainContextMenu.addAction('Eliminar', lambda: self._remove_second_level_node(index))
        _mainContextMenu.addSeparator()
        if self._actions.timer_is_active(index):
            _mainContextMenu.addAction('Pausar cuenta atras',
                                       lambda: self._actions.pause_timer(index))
            _mainContextMenu.addAction('Detener cuenta atras',
                                       lambda: self._actions.stop_timer(index))
        else:
            if self._actions.time_span_is_zero(index):
                _mainContextMenu.addAction('Comenzar cuenta atras',
                                           lambda: self._actions.start_timer(index))
            else:
                _mainContextMenu.addAction('Reanudar cuenta atras',
                                           lambda: self._actions.resume_timer(index))
                _mainContextMenu.addAction('Reiniciar cuenta atras',
                                           lambda: self._actions.start_timer(index))
                _mainContextMenu.addAction('Detener cuenta atras',
                                           lambda: self._actions.stop_timer(index))
            _mainContextMenu.addSeparator()
            if self._actions.state_is_on(index):
                _mainContextMenu.addAction('Apagado Manual',
                                           lambda: self._actions.set_state(index, False))
            else:
                _mainContextMenu.addAction('Encendido Manual',
                                           lambda: self._actions.set_state(index, True))
        _mainContextMenu.exec_(self.mapToGlobal(point))

    # ----------------------------------------------------------------------------------------------------

    @staticmethod
    def _get_item_level(index):
        parent = index.model().itemFromIndex(index).parent()
        count = 0
        while parent:
            count += 1
            parent = parent.parent()
        return count

        # -------------------------------------------------------------------------------
