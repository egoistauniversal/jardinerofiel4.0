from PyQt4 import QtCore, QtGui
from StandardItems import groupStandardItems


class SensorActions(QtCore.QObject):

    @staticmethod
    def add_first_level_node(model, group_id, group_name):
        model.item(0, 0).appendRow(groupStandardItems.StandardItemNameID(group_id, group_name))