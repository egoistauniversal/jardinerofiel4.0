from PyQt4 import QtCore, QtGui
from StandardItems import componentStandardItems


class ComponentActions(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)


    @staticmethod
    def add_clock_node(index, c_id, c_name, c_type, c_time_on, c_time_off, c_pin, c_active, serial):
        _nameItem = componentStandardItems.StandardItemNameID(c_id, c_name)
        _timeTypeItem = componentStandardItems.StandardItemType(c_type)
        _dateTimeOn = componentStandardItems.StandardItemDateTime(c_time_on)
        _dateTimeOff = componentStandardItems.StandardItemDateTime(c_time_off)
        _timeSpanItem = componentStandardItems.StandardItemClockDateTimeSpan()
        _stateItem = componentStandardItems.StandardItemState(serial)
        _pinItem = componentStandardItems.StandardItemPin(c_pin)
        _activeItem = componentStandardItems.StandardItemActive(c_active)

        item = index.model().itemFromIndex(index)
        item.appendRow([_nameItem, _timeTypeItem, _dateTimeOn, _dateTimeOff,
                        _timeSpanItem, _stateItem, _pinItem, _activeItem])

        # if Active column is True then start timer
        if item.child(item.rowCount() - 1, 7).is_active():
            # Start StandardItemTimeSpan timer
            item.child(item.rowCount() - 1, 4).start_timer()

    @staticmethod
    def modify_clock_node(index, c_name, c_time_on, c_time_off, c_pin):
        # Stop count-down
        index.model().itemFromIndex(index.parent().child(index.row(), 4)).stop_timer()

        index.model().itemFromIndex(index.parent().child(index.row(), 0)).set_name(c_name)
        index.model().itemFromIndex(index.parent().child(index.row(), 2)).set_date_time_from_string(c_time_on)
        index.model().itemFromIndex(index.parent().child(index.row(), 3)).set_date_time_from_string(c_time_off)
        index.model().itemFromIndex(index.parent().child(index.row(), 6)).set_pin(c_pin)

        # if Active column is True then start timer
        if index.model().itemFromIndex(index.parent().child(index.row(), 7)).is_active():
            index.model().itemFromIndex(index.parent().child(index.row(), 4)).clear_text()
            # Start count-down
            index.model().itemFromIndex(index.parent().child(index.row(), 4)).start_timer()

    # ------------------------------------------TIMER-----------------------------------------------

    @staticmethod
    def add_timer_node(index, c_id, c_name, c_type, c_time_on, c_time_off, c_pin, c_active, serial):
        _nameItem = componentStandardItems.StandardItemNameID(c_id, c_name)
        _timeTypeItem = componentStandardItems.StandardItemType(c_type)
        _timeOn = componentStandardItems.StandardItemTime(c_time_on)
        _timeOff = componentStandardItems.StandardItemTime(c_time_off)
        _timeSpanItem = componentStandardItems.StandardItemTimerTimeSpan()
        _stateItem = componentStandardItems.StandardItemState(serial)
        _pinItem = componentStandardItems.StandardItemPin(c_pin)
        _activeItem = componentStandardItems.StandardItemActive(c_active)

        item = index.model().itemFromIndex(index)
        item.appendRow([_nameItem, _timeTypeItem, _timeOn, _timeOff,
                        _timeSpanItem, _stateItem, _pinItem, _activeItem])

        # if Active column is True then start timer
        if item.child(item.rowCount() - 1, 7).is_active():
            # Start StandardItemTimeSpan timer
            item.child(item.rowCount() - 1, 4).start_timer()

    def modify_timer_node(self, index, c_name, c_time_on, c_time_off, c_pin, reset):
        index.model().itemFromIndex(index.parent().child(index.row(), 0)).set_name(c_name)
        index.model().itemFromIndex(index.parent().child(index.row(), 2)).set_time(c_time_on)
        index.model().itemFromIndex(index.parent().child(index.row(), 3)).set_time(c_time_off)
        index.model().itemFromIndex(index.parent().child(index.row(), 6)).set_pin(c_pin)

        # if Active column is True then start timer
        if index.model().itemFromIndex(index.parent().child(index.row(), 7)).is_active():
            if reset:
                if reset == 1:
                    self.set_state(index, True)
                    self.set_time_on(index)
                elif reset == 2:
                    self.set_state(index, False)
                    self.set_time_off(index)

    # ------------------------------------------PULSAR-----------------------------------------------

    @staticmethod
    def add_pulsar_node(index, c_id, c_name, c_type, c_time_on, c_pin, c_active, serial):
        _nameItem = componentStandardItems.StandardItemNameID(c_id, c_name)
        _timeTypeItem = componentStandardItems.StandardItemType(c_type)
        _timeOn = componentStandardItems.StandardItemTime(c_time_on)
        _timeOff = QtGui.QStandardItem('')
        _timeSpanItem = componentStandardItems.StandardItemPulsarTimeSpan()
        _stateItem = componentStandardItems.StandardItemState(serial)
        _pinItem = componentStandardItems.StandardItemPin(c_pin)
        _activeItem = componentStandardItems.StandardItemActive(c_active)

        item = index.model().itemFromIndex(index)
        item.appendRow([_nameItem, _timeTypeItem, _timeOn, _timeOff,
                        _timeSpanItem, _stateItem, _pinItem, _activeItem])

    def modify_pulsar_node(self, index, c_name, c_time_on, c_pin, reset):
        index.model().itemFromIndex(index.parent().child(index.row(), 0)).set_name(c_name)
        index.model().itemFromIndex(index.parent().child(index.row(), 2)).set_time(c_time_on)
        index.model().itemFromIndex(index.parent().child(index.row(), 6)).set_pin(c_pin)
        if reset == 1:
            self.start_timer(index)

    # ------------------------------------------REMOVE-----------------------------------------------

    def remove_item_from_group(self, parent_index):
        _item = parent_index.model().itemFromIndex(parent_index)
        if _item.hasChildren():
            _rows = _item.rowCount()
            for i in xrange(_rows):
                _childIndex = _item.child(0, 0).index()
                self.remove_second_level_node(_childIndex)

    def remove_second_level_node(self, index):
        if self.timer_is_active(index):
            self.stop_timer(index)
        if self.state_is_on(index):
            self.set_state(index, False)
        parent = index.model().itemFromIndex(index).parent()
        # Remove node from group
        parent.removeRow(index.row())

    # --------------------------------------------GENERAL------------------------------------------

    @staticmethod
    def get_row_data(index):
        # Get group_id from index's parent
        _group_id = index.model().itemFromIndex(index.parent()).get_id()
        # Get data from index
        _id = index.model().itemFromIndex(index.parent().child(index.row(), 0)).get_id()
        _name = index.model().itemFromIndex(index.parent().child(index.row(), 0)).get_name()
        _timeType = index.model().itemFromIndex(index.parent().child(index.row(), 1)).get_type()
        # get_time_string() from StandardItemDateTime and from StandardItemTime
        _timeOn = index.model().itemFromIndex(index.parent().child(index.row(), 2)).get_time_string()
        # get_time_string() from StandardItemDateTime and from StandardItemTime
        _timeOff = index.model().itemFromIndex(index.parent().child(index.row(), 3)).get_time_string()
        _pin = index.model().itemFromIndex(index.parent().child(index.row(), 6)).data(
            QtCore.Qt.DisplayRole).toString()

        _list = [_group_id, _id, _name, _timeType, _timeOn, _timeOff, _pin]
        return _list

    @staticmethod
    def get_pulsar_row_data(index):
        # Get group_id from index's parent
        _group_id = index.model().itemFromIndex(index.parent()).get_id()
        # Get data from index
        _id = index.model().itemFromIndex(index.parent().child(index.row(), 0)).get_id()
        _name = index.model().itemFromIndex(index.parent().child(index.row(), 0)).get_name()
        _timeType = index.model().itemFromIndex(index.parent().child(index.row(), 1)).get_type()
        # get_time_string() from StandardItemDateTime and from StandardItemTime
        _timeOn = index.model().itemFromIndex(index.parent().child(index.row(), 2)).get_time_string()
        # get_time_string() from StandardItemDateTime and from StandardItemTime
        _pin = index.model().itemFromIndex(index.parent().child(index.row(), 6)).data(
            QtCore.Qt.DisplayRole).toString()

        _list = [_group_id, _id, _name, _timeType, _timeOn, _pin]
        return _list

    @staticmethod
    def get_remove_data(index):
        _id = index.model().itemFromIndex(index.parent().child(index.row(), 0)).get_id()
        _name = index.model().itemFromIndex(index.parent().child(index.row(), 0)).get_name()

        _list = [_id, _name]
        return _list

    @staticmethod
    def get_active_data(index):
        # Get group_id from index's parent
        _id = index.model().itemFromIndex(index.parent().child(index.row(), 0)).get_id()
        _name = index.model().itemFromIndex(index.parent().child(index.row(), 0)).get_name()
        _active = index.model().itemFromIndex(index.parent().child(index.row(), 7)).is_active()

        _list = [_id, _name, _active]
        return _list

    @staticmethod
    def get_type(index):
        return index.model().itemFromIndex(index.parent().child(index.row(), 1)).get_type()

    @staticmethod
    def set_state(index, c_state):
        index.model().itemFromIndex(index.parent().child(index.row(), 5)).set_state(c_state)

    @staticmethod
    def set_time_on(index):
        index.model().itemFromIndex(index.parent().child(index.row(), 4)).set_time_on()

    @staticmethod
    def set_time_off(index):
        index.model().itemFromIndex(index.parent().child(index.row(), 4)).set_time_off()

    @staticmethod
    def state_is_on(index):
        return index.model().itemFromIndex(index.parent().child(index.row(), 5)).is_on()

    def set_active(self, index, c_active):
        # Set active column to True or False
        index.model().itemFromIndex(index.parent().child(index.row(), 7)).set_active(c_active)
        # if c_active is True
        if c_active:
            # Start count-down
            index.model().itemFromIndex(index.parent().child(index.row(), 4)).start_timer()
        else:
            # Strop count-down
            index.model().itemFromIndex(index.parent().child(index.row(), 4)).stop_timer()
            if index.model().itemFromIndex(index.parent().child(index.row(), 1)).get_type() == '1':
                index.model().itemFromIndex(index.parent().child(index.row(), 4)).clear_text()
            self.set_state(index, c_active)

    @staticmethod
    def start_timer(index):
        index.model().itemFromIndex(index.parent().child(index.row(), 4)).start_timer()

    @staticmethod
    def resume_timer(index):
        index.model().itemFromIndex(index.parent().child(index.row(), 4)).resume_timer()

    @staticmethod
    def stop_timer(index):
        index.model().itemFromIndex(index.parent().child(index.row(), 4)).stop_timer()

    @staticmethod
    def pause_timer(index):
        index.model().itemFromIndex(index.parent().child(index.row(), 4)).pause_timer()

    @staticmethod
    def timer_is_active(index):
        return index.model().itemFromIndex(index.parent().child(index.row(), 4)).timer_is_active()

    @staticmethod
    def time_span_is_zero(index):
        return index.model().itemFromIndex(index.parent().child(index.row(), 4)).time_span_is_zero()

    @staticmethod
    def is_active(index):
        return index.model().itemFromIndex(index.parent().child(index.row(), 7)).is_active()

    def resume_countdown_with_time_on(self, index):
        self.set_time_on(index)
        self.start_timer(index)

    def resume_countdown_with_time_off(self, index):
        self.set_time_off(index)
        self.start_timer(index)