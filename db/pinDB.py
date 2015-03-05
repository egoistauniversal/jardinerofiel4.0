from PyQt4 import QtCore
import sqlite3


class ComponentControl(QtCore.QObject):
    def __init__(self, browser, dbfile):
        QtCore.QObject.__init__(self)
        self._browser = browser
        self._dbfile = dbfile

    def create_table(self):
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("CREATE TABLE pins_component_control("
                               "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                               "value TEXT NOT NULL, "
                               "enabled INTEGER NOT NULL)")

                _list = ['23', '25', '27', '29', '31', '33', '35', '37']
                for _pin in _list:
                    cursor.execute("INSERT INTO pins_component_control VALUES (NULL, ?, ?)",
                                   (_pin, 1))
        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.create_table.__name__)

    def select_all_pins(self):
        _list = []
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("SELECT pins_component_control.value FROM pins_component_control "
                               "WHERE pins_component_control.enabled=1", )
                _rows = cursor.fetchall()
                for _row in _rows:
                    _list.append(_row[0])
        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.select_all_pins.__name__)
        return _list

    def select_used_pins(self, group_id):
        _list = []
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("SELECT component.pin FROM component "
                               "WHERE component.group_id=? AND component.enabled=1", (group_id, ))
                _rows = cursor.fetchall()
                for _row in _rows:
                    _list.append(_row[0])

                cursor.execute("SELECT control.pin FROM control "
                               "WHERE control.group_id=? and control.enabled=1", (group_id, ))
                _rows = cursor.fetchall()
                for _row in _rows:
                    _list.append(_row[0])
        except sqlite3.Error, e:
            self._browser.print_alert_message(
                e.args[0] + ' in ' + self.select_used_pins.__name__)
        return _list

    def _print_alert_message(self, error, class_name, method_name):
        self._browser.print_alert_message(error + ' in Class = ' + class_name + ' Method = ' + method_name)

# ------------------------------------------------------------------------------------------------------


class SensorFertilizer(QtCore.QObject):
    def __init__(self, browser, dbfile):
        QtCore.QObject.__init__(self)
        self._browser = browser
        self._dbfile = dbfile

    def create_table(self):
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("CREATE TABLE pins_sensor_fertilizer("
                               "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                               "value TEXT NOT NULL, "
                               "enabled INTEGER NOT NULL)")

                _list = ['A8', 'A9', '22', '24']
                for _pin in _list:
                    cursor.execute("INSERT INTO pins_sensor_fertilizer VALUES (NULL, ?, ?)",
                                   (_pin, 1))
        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.create_table.__name__)

    def _print_alert_message(self, error, class_name, method_name):
        self._browser.print_alert_message(error + ' in Class = ' + class_name + ' Method = ' + method_name)