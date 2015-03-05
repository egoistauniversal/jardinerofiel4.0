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
        self._setup_database()

    def _setup_database(self):
        # if file is empty create tables
        if self._mainDBFile.size() == 0:
            groupNodeDB.GroupNodeDB(self._browser, self._mainDBFile.fileName()).create_table()
            componentDB.ComponentDB(self._browser, self._mainDBFile.fileName()).create_table()
            sensorDB.SensorDB(self._browser, self._mainDBFile.fileName()).create_table()
            controlDB.ControlDB(self._browser, self._mainDBFile.fileName()).create_table()
            pinDB.ComponentControl(self._browser, self._mainDBFile.fileName()).create_table()
            pinDB.SensorFertilizer(self._browser, self._mainDBFile.fileName()).create_table()

    # --------------------------------------------------READ STRUCTURE-----------------------------------------------

    def read_component_structure(self, model):
        componentDB.ComponentDB(self._browser, self._mainDBFile.fileName()).read_structure(model)

    def read_sensor_structure(self, model):
        sensorDB.SensorDB(self._browser, self._mainDBFile.fileName()).read_structure(model)

    # ---------------------------------GROUP TABLE-------------------------------------------

    def group_node_table_name_exist(self, group_name):
        return groupNodeDB.GroupNodeDB(self._browser, self._mainDBFile.fileName()).name_exist(group_name)

    def group_node_table_insert_row(self, group_name):
        return groupNodeDB.GroupNodeDB(self._browser, self._mainDBFile.fileName()).insert_row(group_name)

    def group_node_table_modify_row(self, group_id, new_name):
        groupNodeDB.GroupNodeDB(self._browser, self._mainDBFile.fileName()).modify_row(group_id, new_name)

    def group_node_table_remove_row(self, group_id):
        groupNodeDB.GroupNodeDB(self._browser, self._mainDBFile.fileName()).remove_row(group_id)

    # ---------------------------------COMPONENTS TABLE-------------------------------------------

    def component_table_name_exist(self, group_id, name):
        return componentDB.ComponentDB(self._browser, self._mainDBFile.fileName()).name_exist(group_id, name)

    def component_table_insert_row(self, group_id, c_name, c_type, c_on, c_off, c_pin, c_active):
        return componentDB.ComponentDB(self._browser, self._mainDBFile.fileName()).insert_row(group_id, c_name, c_type,
                                                                                              c_on,
                                                                                              c_off, c_pin, c_active)

    def component_table_modify_row(self, c_id, c_name, c_on, c_off, c_pin):
        componentDB.ComponentDB(self._browser, self._mainDBFile.fileName()).modify_row(c_id, c_name, c_on,
                                                                                       c_off, c_pin)

    def component_table_modify_column_active(self, c_id, c_active):
        componentDB.ComponentDB(self._browser, self._mainDBFile.fileName()).modify_active_column(c_id, c_active)

    def component_table_remove_row_by_id(self, c_id):
        componentDB.ComponentDB(self._browser, self._mainDBFile.fileName()).remove_row_by_id(c_id)

    def component_table_remove_row_by_group_id(self, group_id):
        componentDB.ComponentDB(self._browser, self._mainDBFile.fileName()).remove_row_by_group_id(group_id)

    # ---------------------------------PINS_COMPONENT_CONTROL TABLE------------------------------------------

    def pins_component_control_select_all(self):
        return pinDB.ComponentControl(self._browser, self._mainDBFile.fileName()).select_all_pins()

    def pins_component_control_table_select_pin_used(self, group_id):
        return pinDB.ComponentControl(self._browser, self._mainDBFile.fileName()).select_used_pins(group_id)

        # ---------------------------------PINS_SENSOR_FERTILIZER TABLE------------------------------------------