from PyQt4 import QtCore
import sqlite3


class ControlDB(QtCore.QObject):
    def __init__(self, browser, dbfile):
        QtCore.QObject.__init__(self)
        self._browser = browser
        self._dbfile = dbfile

    def create_table(self):
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("CREATE TABLE control("
                               "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                               "group_id INTEGER NOT NULL, "
                               "control_type TEXT NOT NULL, "
                               "x_name TEXT NOT NULL, "
                               "x_type TEXT NOT NULL, "
                               "operator TEXT NOT NULL, "
                               "goal_value TEXT NOT NULL, "
                               "device_name TEXT NOT NULL, "
                               "pause TEXT NOT NULL, "
                               "protocol TEXT NOT NULL, "
                               "pin TEXT NOT NULL, "
                               "active INTEGER NOT NULL, "
                               "enabled INTEGER NOT NULL)")
        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.create_table.__name__)

    def _print_alert_message(self, error, class_name, method_name):
        self._browser.print_alert_message(error + ' in Class = ' + class_name + ' Method = ' + method_name)