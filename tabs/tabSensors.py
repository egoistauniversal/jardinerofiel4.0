from PyQt4 import QtGui, QtCore
from dialogbox import sensorDialogBox
from misc import treeView
from actions import groupActions


class TabSensors(QtGui.QWidget):
    def __init__(self, db, serial, browser):
        super(TabSensors, self).__init__()
        self._model = QtGui.QStandardItemModel(0, 11, self)
        self._mainDB = db
        self._serial = serial
        self._browser = browser
        self._myTreeView = treeView.TreeView()
        self._setup()

    def _setup(self):
        self._setup_model()
        self._setup_layouts()
        self._setup_connections()
        self._mainDB.read_sensor_structure(self._model)

    def _setup_model(self):
        self._model.setHeaderData(0, QtCore.Qt.Horizontal, 'Nombre')
        self._model.setHeaderData(1, QtCore.Qt.Horizontal, 'Tipo')
        self._model.setHeaderData(2, QtCore.Qt.Horizontal, 'Dato Actual')
        self._model.setHeaderData(3, QtCore.Qt.Horizontal, 'Minimo')
        self._model.setHeaderData(4, QtCore.Qt.Horizontal, 'Hora')
        self._model.setHeaderData(5, QtCore.Qt.Horizontal, 'Fecha')
        self._model.setHeaderData(6, QtCore.Qt.Horizontal, 'Maximo')
        self._model.setHeaderData(7, QtCore.Qt.Horizontal, 'Hora')
        self._model.setHeaderData(8, QtCore.Qt.Horizontal, 'Fecha')
        self._model.setHeaderData(9, QtCore.Qt.Horizontal, 'Pin')
        self._model.setHeaderData(10, QtCore.Qt.Horizontal, 'Programado')
        self._model.appendRow(QtGui.QStandardItem('Sensores'))
        self._myTreeView.setModel(self._model)

    def _setup_layouts(self):
        _treeViewLayout = QtGui.QHBoxLayout()
        _treeViewLayout.addWidget(self._myTreeView)
        self.setLayout(_treeViewLayout)

    def _setup_connections(self):
        pass

    # -------------------------------------------GROUP_NODE--------------------------------------------------------

    def add_group_node(self, group_id, group_name):
        groupActions.GroupActions().add(self._model, group_id, group_name)

    def modify_group_node(self, index, group_name):
        groupActions.GroupActions().modify(self._model, index, group_name)

    def remove_group_node(self, index, group_id):
        groupActions.GroupActions().remove(self._model, index)