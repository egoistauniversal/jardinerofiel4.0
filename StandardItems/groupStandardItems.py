from PyQt4 import QtGui


class StandardItemGroup(QtGui.QStandardItem):
    def __init__(self, c_id, c_name):
        super(StandardItemGroup, self).__init__()
        self._name = None
        self._id = None

        self.set_name(c_name)
        self.set_id(c_id)

    def set_name(self, name):
        self._name = name
        self.setText(self._name)

    def set_id(self, c_id):
        self._id = c_id
        self.setToolTip('group_id=' + str(self._id))

    def get_name(self):
        return self._name

    def get_id(self):
        return self._id
