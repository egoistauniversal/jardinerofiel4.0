from PyQt4 import QtCore, QtGui


class TreeView(QtGui.QTreeView):
    def __init__(self):
        super(TreeView, self).__init__()
        self._setup()

    def _setup(self):
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setItemsExpandable(True)

    def edit(self, index, trigger, event):
        if trigger == QtGui.QAbstractItemView.DoubleClicked:
            # print 'DoubleClick Killed!'
            return False
        return QtGui.QTreeView.edit(self, index, trigger, event)