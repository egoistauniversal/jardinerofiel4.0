from PyQt4 import QtCore
import sqlite3


class ComponentDB(QtCore.QObject):
    def __init__(self, browser, dbfile):
        QtCore.QObject.__init__(self)
        self._browser = browser
        self._dbfile = dbfile

    def create_table(self):
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("CREATE TABLE component("
                               "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                               "group_id INTEGER NOT NULL, "
                               "name TEXT NOT NULL, "
                               "type INTEGER NOT NULL, "
                               "switch_on TEXT NOT NULL, "
                               "switch_off TEXT NOT NULL, "
                               "pin INTEGER NOT NULL, "
                               "active INTEGER NOT NULL, "
                               "enabled INTEGER NOT NULL)")
        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.create_table.__name__)

    def read_structure(self, model, serial):
        from db import groupNodeDB
        from actions import groupActions, componentActions

        group_rows = groupNodeDB.GroupNodeDB(self._browser, self._dbfile).select_all()
        for group_row in group_rows:
            # group_row[0] = ID; group_row[1] = Radio; group_row[2] = Name
            groupActions.GroupActions.add(model, group_row[0], group_row[1], group_row[2])
            component_rows = self.select_row_by_group_id(group_row[0])
            for row in component_rows:
                model_row_count = model.item(0, 0).rowCount() - 1
                _index = model.item(0, 0).child(model_row_count, 0).index()
                if row[2] == 1:
                    componentActions.ComponentActions.add_clock_node(_index, row[0], row[1], row[2],
                                                                     QtCore.QString(row[3]),
                                                                     QtCore.QString(row[4]),
                                                                     row[5], row[6], serial)
                elif row[2] == 2:
                    componentActions.ComponentActions.add_timer_node(_index, row[0], row[1], row[2],
                                                                     QtCore.QString(row[3]),
                                                                     QtCore.QString(row[4]),
                                                                     row[5], row[6], serial)
                elif row[2] == 3:
                    componentActions.ComponentActions.add_pulsar_node(_index, row[0], row[1], row[2],
                                                                      QtCore.QString(row[3]),
                                                                      row[5], row[6], serial)

    def select_row_by_group_id(self, group_id):
        _rows = None
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("SELECT component.id, component.name, component.type, component.switch_on, "
                               "component.switch_off, component.pin, component.active "
                               "FROM component "
                               "WHERE component.group_id=? "
                               "AND component.enabled=1", (group_id,))
                _rows = cursor.fetchall()
        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.select_row_by_group_id.__name__)
        return _rows

    def name_exist(self, group_id, name):
        _exist = False
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("SELECT component.id FROM component "
                               "WHERE component.group_id=? AND component.name=? AND component.enabled=1",
                               (group_id, name))
                if len(cursor.fetchall()) > 0:
                    _exist = True
        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.name_exist.__name__)
        return _exist

    def insert_row(self, group_id, c_name, c_type, c_on, c_off, c_pin, c_active):
        _id = -1
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO component VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (group_id, c_name, c_type, c_on, c_off, c_pin, c_active, 1))
                cursor.execute("SELECT last_insert_rowid()")
                row = cursor.fetchone()
                _id = row[0]
        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.insert_row.__name__)
        return _id

    def modify_row(self, c_id, c_name, c_on, c_off, c_pin):
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cur = connection.cursor()
                cur.execute("UPDATE component SET name=?, switch_on=?, switch_off=?, pin=? "
                            "WHERE component.id=?",
                            (c_name, c_on, c_off, c_pin, c_id))
        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.modify_row.__name__)

    def modify_active_column(self, c_id, c_active):
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("UPDATE component SET active=? WHERE component.id=? AND component.enabled=1",
                               (c_active, c_id))
        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.modify_active_column.__name__)

    def remove_row_by_id(self, c_id):
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("UPDATE component SET enabled=0 "
                               "WHERE component.id=? AND component.enabled=1", (c_id,))
        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.remove_row_by_id.__name__)

    def remove_row_by_group_id(self, group_id):
        try:
            connection = sqlite3.connect(str(self._dbfile))
            with connection:
                cursor = connection.cursor()
                cursor.execute("UPDATE component SET enabled=0 "
                               "WHERE component.group_id=? AND component.enabled=1", (group_id,))
        except sqlite3.Error, e:
            self._print_alert_message(e.args[0], self.__class__.__name__, self.remove_row_by_group_id.__name__)

    # ------------------------------------------PRINT----------------------------------------------------

    def _print_alert_message(self, error, class_name, method_name):
        self._browser.print_alert_message(error + ' in Class = ' + class_name + ' Method = ' + method_name)