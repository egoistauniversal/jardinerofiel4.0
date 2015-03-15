from PyQt4 import QtCore
import sqlite3


class SensorDB(QtCore.QObject):
    def __init__(self, browser, dbfile):
        QtCore.QObject.__init__(self)
        self._browser = browser
        self._dbfile = dbfile

    def create_table(self):
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("CREATE TABLE sensor("
                               "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                               "group_id INTEGER NOT NULL, "
                               "name TEXT NOT NULL, "
                               "type INTEGER NOT NULL, "
                               "pin INTEGER NOT NULL, "
                               "active INTEGER NOT NULL, "
                               "enabled INTEGER NOT NULL)")
        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.create_table.__name__)

    def read_structure(self, model):
        from db import groupNodeDB
        from actions import groupActions

        group_rows = groupNodeDB.GroupNodeDB(self._browser, self._dbfile).select_all()
        for group_row in group_rows:
            # group_row[0] = ID; group_row[1] = Name
            groupActions.GroupActions.add(model, group_row[0], group_row[1], group_row[2])

    def _print_alert_message(self, error, class_name, method_name):
        self._browser.print_alert_message(error + ' in Class = ' + class_name + ' Method = ' + method_name)