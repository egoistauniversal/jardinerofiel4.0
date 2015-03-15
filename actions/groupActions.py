from PyQt4 import QtCore, QtGui
from StandardItems import groupStandardItems


class GroupActions(QtCore.QObject):
    @staticmethod
    def add(model, group_id, group_radio, group_name):
        model.item(0, 0).appendRow(groupStandardItems.StandardItemGroup(group_id, group_radio, group_name))

    @staticmethod
    def modify(model, index, group_radio, group_name):
        model.item(0, 0).child(index.row(), 0).set_name(group_name)
        model.item(0, 0).child(index.row(), 0).set_radio(group_radio)

    @staticmethod
    def remove(model, index):
        model.item(0, 0).removeRow(index.row())
