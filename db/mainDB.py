from PyQt4 import QtCore
from db import groupNodeDB, componentDB, sensorDB, controlDB, pinDB


class DataBase(QtCore.QObject):
    def __init__(self, browser):
        QtCore.QObject.__init__(self)
        self._browser = browser
        # find user home directory
        self._directory = QtCore.QDir(QtCore.QDir().home().path() + '/jf/db')
        # Create directory if it doesn't exist
        if not self._directory.exists():
            QtCore.QDir().mkpath(self._directory.path())
        self._mainDBName = QtCore.QString('/jardinerofiel.sqlite')
        self._mainDBFile = QtCore.QFile(self._directory.path() + self._mainDBName)
        self._groupNodeDB = groupNodeDB.GroupNodeDB(self._browser, self._mainDBFile.fileName())
        self._componentDB = componentDB.ComponentDB(self._browser, self._mainDBFile.fileName())
        self._sensorDB = sensorDB.SensorDB(self._browser, self._mainDBFile.fileName())
        self._controlDB = controlDB.ControlDB(self._browser, self._mainDBFile.fileName())
        self._pinDBComponentControl = pinDB.ComponentControl(self._browser, self._mainDBFile.fileName())
        self._pinDBSensorFertilizer = pinDB.SensorFertilizer(self._browser, self._mainDBFile.fileName())
        self._setup_database()

    def _setup_database(self):
        # if file is empty create tables
        if self._mainDBFile.size() == 0:
            self._groupNodeDB.create_table()
            self._componentDB.create_table()
            self._sensorDB.create_table()
            self._controlDB.create_table()
            self._pinDBComponentControl.create_table()
            self._pinDBSensorFertilizer.create_table()

    # --------------------------------------------------READ STRUCTURE-----------------------------------------------

    def read_component_structure(self, model, serial):
        self._componentDB.read_structure(model, serial)

    def read_sensor_structure(self, model):
        self._sensorDB.read_structure(model)

    # ---------------------------------GROUP TABLE-------------------------------------------

    def group_node_table_name_exist(self, group_name):
        return self._groupNodeDB.name_exist(group_name)

    def group_node_table_insert_row(self, group_name):
        return self._groupNodeDB.insert_row(group_name)

    def group_node_table_modify_row(self, group_id, new_name):
        self._groupNodeDB.modify_row(group_id, new_name)

    def group_node_table_remove_row(self, group_id):
        self._groupNodeDB.remove_row(group_id)

    # ---------------------------------COMPONENTS TABLE-------------------------------------------

    def component_table_name_exist(self, group_id, name):
        return self._componentDB.name_exist(group_id, name)

    def component_table_insert_row(self, group_id, c_name, c_type, c_on, c_off, c_pin, c_active):
        return self._componentDB.insert_row(group_id, c_name, c_type, c_on, c_off, c_pin, c_active)

    def component_table_modify_row(self, c_id, c_name, c_on, c_off, c_pin):
        self._componentDB.modify_row(c_id, c_name, c_on, c_off, c_pin)

    def component_table_modify_column_active(self, c_id, c_active):
        self._componentDB.modify_active_column(c_id, c_active)

    def component_table_remove_row_by_id(self, c_id):
        self._componentDB.remove_row_by_id(c_id)

    def component_table_remove_row_by_group_id(self, group_id):
        self._componentDB.remove_row_by_group_id(group_id)

    # ---------------------------------PINS_COMPONENT_CONTROL TABLE------------------------------------------

    def pins_component_control_select_all(self):
        return self._pinDBComponentControl.select_all_pins()

    def pins_component_control_table_select_pin_used(self, group_id):
        return self._pinDBComponentControl.select_used_pins(group_id)

        # ---------------------------------PINS_SENSOR_FERTILIZER TABLE------------------------------------------