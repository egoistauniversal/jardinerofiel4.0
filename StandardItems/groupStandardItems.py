from PyQt4 import QtGui


class StandardItemGroup(QtGui.QStandardItem):
    def __init__(self, g_id, g_radio, g_name):
        super(StandardItemGroup, self).__init__()
        self._id = None
        self._radio = None
        self._name = None

        self.set_id(g_id)
        self.set_radio(g_radio)
        self.set_name(g_name)

    def set_id(self, c_id):
        self._id = c_id
        self.set_tooltip(self._id, self._radio)

    def set_radio(self, radio):
        self._radio = radio
        self.set_tooltip(self._id, self._radio)

    def set_name(self, name):
        self._name = name
        self.setText(self._name)

    def get_id(self):
        return self._id

    def get_radio(self):
        return self._radio

    def get_name(self):
        return self._name

    def set_tooltip(self, g_id, g_radio):
        self.setToolTip('ID=' + str(g_id) + '<br>Radio=' + str(g_radio))
