from PyQt4 import QtCore
import sqlite3


class GroupNodeDB(QtCore.QObject):
    def __init__(self, browser, dbfile):
        QtCore.QObject.__init__(self)
        self._browser = browser
        self._dbfile = dbfile

    def create_table(self):
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("CREATE TABLE group_node("
                               "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                               "radio INTEGER NOT NULL, "
                               "name TEXT NOT NULL, "
                               "enabled INTEGER NOT NULL)")
        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.create_table.__name__)

    def select_all(self):
        _rows = None
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("SELECT group_node.id, group_node.radio, group_node.name FROM group_node "
                               "WHERE group_node.enabled=1")
                _rows = cursor.fetchall()
        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.select_all.__name__)
        return _rows

    def select_used_radio(self):
        _list = []
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("SELECT group_node.radio FROM group_node "
                               "WHERE group_node.enabled=1")
                _rows = cursor.fetchall()
                for _row in _rows:
                    _list.append(_row[0])
        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.select_used_radio.__name__)
        return _list

    def name_exist(self, group_name):
        _exist = False
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("SELECT group_node.id FROM group_node WHERE group_node.name=? "
                               "AND group_node.enabled=1",
                               (group_name,))
                if len(cursor.fetchall()) > 0:
                    _exist = True
        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.name_exist.__name__)
        return _exist

    def insert_row(self, group_radio, group_name):
        _id = -1
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO group_node VALUES (NULL, ?, ?, ?)",
                               (group_radio, group_name, 1))
                cursor.execute("SELECT last_insert_rowid()")
                _row = cursor.fetchone()
                _id = _row[0]
        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.insert_row.__name__)
        return _id

    def modify_row(self, group_id, group_radio, new_name):
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("UPDATE group_node SET radio=?, name=? WHERE group_node.id=? AND group_node.enabled=1",
                               (group_radio, new_name, group_id))
        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.modify_row.__name__)

    def remove_row(self, group_id):
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("UPDATE group_node SET enabled=0 WHERE group_node.id=? AND group_node.enabled=1",
                               (group_id,))

        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.remove_row.__name__)

    def _print_alert_message(self, error, class_name, method_name):
        self._browser.print_alert_message(error + ' in Class = ' + class_name + ' Method = ' + method_name)