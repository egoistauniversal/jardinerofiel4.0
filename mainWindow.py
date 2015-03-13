from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from misc import serialUSB, browser
from tabs import tabComponents, tabSensors
from messagebox import mainWindow
from db import mainDB


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._tabs = QtGui.QTabWidget(self)
        self._browser = browser.Browser()
        self._serial = serialUSB.SerialUSB(self._browser)

        self._mainDB = mainDB.DataBase(self._browser)
        self._tabComponents = tabComponents.TabComponents(self._mainDB, self._serial, self._browser)
        self._tabSensors = tabSensors.TabSensors(self._mainDB, self._serial, self._browser)
        self._setup()

    def _setup(self):
        self._setup_tabs()
        self._setup_user_interface()
        self._setup_connections()

    def _setup_tabs(self):
        self._tabs.addTab(self._tabComponents, 'Componentes')
        self._tabs.addTab(self._tabSensors, 'Sensores')

    def _setup_user_interface(self):
        self.setWindowTitle('Jardinero Fiel V4.0')
        self.showMaximized()
        self.setCentralWidget(self._tabs)
        _dockBrowser = QtGui.QDockWidget('Log', self)
        # Disable dock's close button
        _dockBrowser.setFeatures(QtGui.QDockWidget.DockWidgetFloatable | QtGui.QDockWidget.DockWidgetMovable)
        _dockBrowser.setMaximumHeight(300)
        _dockBrowser.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        _dockBrowser.setWidget(self._browser)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, _dockBrowser)

        self.statusBar().showMessage('Ready')

    def _setup_connections(self):
        self._tabComponents.insertGroupSignal.connect(self._on_insert_group)
        self._tabComponents.modifyGroupSignal.connect(self._on_modify_group)
        self._tabComponents.removeGroupSignal.connect(self._on_remove_group)

    # ----------------------------------SIGNALS-------------------------------------------------------
    @pyqtSlot(int, str)
    def _on_insert_group(self, group_id, group_name):
        self._tabComponents.add_group_node(group_id, group_name)
        self._tabSensors.add_group_node(group_id, group_name)

    @pyqtSlot(int, str)
    def _on_modify_group(self, index, group_name):
        self._tabComponents.modify_group_node(index, group_name)
        self._tabSensors.modify_group_node(index, group_name)

    @pyqtSlot(int)
    def _on_remove_group(self, index, group_id):
        self._tabComponents.remove_group_node(index, group_id)
        self._tabSensors.remove_group_node(index, group_id)

    def closeEvent(self, event):
        _reply = mainWindow.MessageBox().close_app(self)
        if _reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()