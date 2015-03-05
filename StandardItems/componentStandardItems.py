from PyQt4 import QtCore, QtGui
from misc import icons


class StandardItemNameID(QtGui.QStandardItem):
    def __init__(self, c_id, c_name):
        super(StandardItemNameID, self).__init__()
        self._name = None
        self._id = None
        self.set_name(c_name)
        self.set_id(c_id)

    def set_name(self, name):
        self._name = name
        self.setText(self._name)

    def set_id(self, c_id):
        self._id = c_id
        self.setToolTip('component_id=' + str(self._id))

    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

# ----------------------------------------StandardItemType---------------------------------------


class StandardItemType(QtGui.QStandardItem):
    def __init__(self, c_type):
        super(StandardItemType, self).__init__()
        self._icons = icons.Icons()
        self._type = None
        self.set_type(c_type)

    def set_type(self, c_type):
        self._type = c_type
        self.setIcon(self._icons.get_component_icon(c_type))
        # TODO set tooltip
        # self.setToolTip(ContextMenuOptions.get_component_context_menu_name_options(int(tag)))

    def get_type(self):
        return self._type

# -----------------------------------StandardItemDateTime---------------------------------------


class StandardItemDateTime(QtGui.QStandardItem):
    def __init__(self, c_time):
        super(StandardItemDateTime, self).__init__()
        self._dateTime = None
        self.set_date_time_from_string(c_time)

    def add_days(self, days):
        _datetime = self._dateTime.addDays(days)
        self.set_date_time(_datetime)

    def set_date_time_from_string(self, c_time):
        _dateTime = QtCore.QDateTime(QtCore.QDate().currentDate(),
                                     QtCore.QTime(int(c_time.mid(0, 2)),
                                                  int(c_time.mid(3, 2)),
                                                  int(c_time.mid(6, 2))))
        self.set_date_time(_dateTime)

    def set_date_time(self, date_time):
        self._dateTime = date_time
        self.setText(self._dateTime.toString("HH:mm:ss dd-MM-yyyy"))

    def set_current_date(self):
        self._dateTime.setDate(QtCore.QDate().currentDate())

    def get_date_time(self):
        return self._dateTime

    def get_date(self):
        return self._dateTime.date()

    def get_time_string(self):
        return self._dateTime.time().toString("HH:mm:ss")

# -----------------------------------StandardItemDateTimeSpan---------------------------------------


class StandardItemClockDateTimeSpan(QtGui.QStandardItem):
    def __init__(self):
        super(StandardItemClockDateTimeSpan, self).__init__()
        self._generalAccess = GeneralAccess()
        self._timer = QtCore.QTimer()
        self._setup()

    def _setup(self):
        self._timer.setInterval(1000)
        self._setup_connections()

    def _setup_connections(self):
        self._timer.timeout.connect(self._timer_timeout)

    def start_timer(self):
        self._calculate_state()
        self._timer.start()

    def stop_timer(self):
        self._timer.stop()

    def clear_text(self):
        self.setText('')

    def timer_is_active(self):
        return self._timer.isActive()

    def pause_timer(self):
        self._timer.stop()

    def _timer_timeout(self):
        if self._generalAccess.state_is_on(self.index()):
            self._calculate_date_time_span(QtCore.QDateTime().currentDateTime(),
                                           self._generalAccess.get_date_time_off(self.index()))
            if self.data(QtCore.Qt.DisplayRole).toTime() <= QtCore.QTime(0, 0, 0, 0):
                self._generalAccess.date_time_off_add_days(self.index(), 1)
                self._generalAccess.set_state(self.index(), False)
        else:
            self._calculate_date_time_span(QtCore.QDateTime().currentDateTime(),
                                           self._generalAccess.get_date_time_on(self.index()))
            if self.data(QtCore.Qt.DisplayRole).toTime() <= QtCore.QTime(0, 0, 0, 0):
                self._generalAccess.date_time_on_add_days(self.index(), 1)
                self._generalAccess.set_state(self.index(), True)

    def _calculate_state(self):
        _state = False
        _currentDateTime = QtCore.QDateTime().currentDateTime()
        self._generalAccess.set_date_time_on_current_date(self.index())
        self._generalAccess.set_date_time_off_current_date(self.index())
        if self._generalAccess.get_date_time_on(self.index()) > self._generalAccess.get_date_time_off(self.index()):
            if _currentDateTime < self._generalAccess.get_date_time_off(self.index()):
                self._generalAccess.date_time_on_add_days(self.index(), 1)
                _state = True
            else:
                if _currentDateTime >= self._generalAccess.get_date_time_on(self.index()):
                    self._generalAccess.date_time_on_add_days(self.index(), 1)
                    self._generalAccess.date_time_off_add_days(self.index(), 1)
                    _state = True
                else:
                    self._generalAccess.date_time_off_add_days(self.index(), 1)
        elif self._generalAccess.get_date_time_on(
                self.index()) <= _currentDateTime < self._generalAccess.get_date_time_off(self.index()):
            self._generalAccess.date_time_on_add_days(self.index(), 1)
            _state = True
        elif self._generalAccess.get_date_time_on(
                self.index()) <= _currentDateTime > self._generalAccess.get_date_time_off(self.index()):
            self._generalAccess.date_time_on_add_days(self.index(), 1)
            self._generalAccess.date_time_off_add_days(self.index(), 1)

        self._generalAccess.set_state(self.index(), _state)

    def _calculate_date_time_span(self, now_date_time, my_date_time):
        # Time span between two QDateTime
        _secondsLeft = now_date_time.secsTo(my_date_time)
        self.setText(QtCore.QDateTime().fromTime_t(_secondsLeft).toString("HH:mm:ss"))

#     -----------------------------------StandardItemState---------------------------------------


class StandardItemState(QtGui.QStandardItem):
    def __init__(self):
        super(StandardItemState, self).__init__()
        self._icons = icons.Icons()
        self._state = None
        self.set_state(False)

    def set_state(self, state):
        self._state = state
        self.setIcon(self._icons.get_state_icon(state))

    def is_on(self):
        return self._state

#     -----------------------------------StandardItemActive---------------------------------------


class StandardItemActive(QtGui.QStandardItem):
    def __init__(self, active):
        super(StandardItemActive, self).__init__()
        self._icons = icons.Icons()
        self._active = None
        self.set_active(active)

    def set_active(self, active):
        self._active = active
        self.setIcon(self._icons.get_active_icon(active))

    def is_active(self):
        return self._active

#     --------------------------------StandardItemTime------------------------------------------


class StandardItemTime(QtGui.QStandardItem):
    def __init__(self, t_time):
        super(StandardItemTime, self).__init__()
        self.set_time(t_time)

    def set_time(self, t_time):
        self.setData(t_time, QtCore.Qt.DisplayRole)

    def get_time(self):
        return self.data(QtCore.Qt.DisplayRole).toTime()

    def get_time_string(self):
        return self.data(QtCore.Qt.DisplayRole).toString()

#     --------------------------------StandardItemTimerSpan------------------------------------------


class StandardItemTimerTimeSpan(QtGui.QStandardItem):
    def __init__(self):
        super(StandardItemTimerTimeSpan, self).__init__()
        self._generalAccess = GeneralAccess()
        self._timer = QtCore.QTimer()
        self._setup()

    def _setup(self):
        self._timer.setInterval(1000)
        self._setup_connections()

    def _setup_connections(self):
        self._timer.timeout.connect(self._timer_timeout)

    def set_time(self, c_time):
        self.setData(c_time.toString("HH:mm:ss"), QtCore.Qt.DisplayRole)

    def set_time_on(self):
        self.set_time(self._generalAccess.get_time_on(self.index()))

    def set_time_off(self):
        self.set_time(self._generalAccess.get_time_off(self.index()))

    def start_timer(self):
        self._timer.start()

    def stop_timer(self):
        self._timer.stop()

    def pause_timer(self):
        self._timer.stop()

    def _timer_timeout(self):
        _state = self._generalAccess.state_is_on(self.index())
        if _state:
            self._count_down(_state)
            # if time left is <= than 0
            if self.data(QtCore.Qt.DisplayRole).toTime() == QtCore.QTime(23, 59, 59, 0):
                self.set_time(self._generalAccess.get_time_off(self.index()))
                self._generalAccess.set_state(self.index(), False)
        else:
            self._count_down(_state)
            # if time left is <= than 0
            if self.data(QtCore.Qt.DisplayRole).toTime() == QtCore.QTime(23, 59, 59, 0):
                self.set_time(self._generalAccess.get_time_on(self.index()))
                self._generalAccess.set_state(self.index(), True)

    def timer_is_active(self):
        return self._timer.isActive()

    def _count_down(self, state):
        if len(self.data(QtCore.Qt.DisplayRole).toString()) > 0:
            _timeLeft = self.data(QtCore.Qt.DisplayRole).toTime()
            _timeLeft = _timeLeft.addMSecs(-self._timer.interval())
            self.set_time(_timeLeft)
        else:
            if state:
                self.set_time(self._generalAccess.get_time_off(self.index()))
                self._generalAccess.set_state(self.index(), False)
            else:
                self.set_time(self._generalAccess.get_time_on(self.index()))
                self._generalAccess.set_state(self.index(), True)

#     --------------------------------StandardItemPulsarTimeSpan------------------------------------------


class StandardItemPulsarTimeSpan(QtGui.QStandardItem):
    def __init__(self):
        super(StandardItemPulsarTimeSpan, self).__init__()
        self._generalAccess = GeneralAccess()
        self._timer = QtCore.QTimer()
        self._setup()

    def _setup(self):
        self.setData('00:00:00', QtCore.Qt.DisplayRole)
        self._timer.setInterval(1000)
        self._setup_connections()

    def _setup_connections(self):
        self._timer.timeout.connect(self._timer_timeout)

    def set_time(self, c_time):
        self.setData(c_time.toString("HH:mm:ss"), QtCore.Qt.DisplayRole)

    def start_timer(self):
        self._timer.start()
        self.set_time(self._generalAccess.get_time_on(self.index()))
        self._generalAccess.set_state(self.index(), True)

    def resume_timer(self):
        if not self._generalAccess.state_is_on(self.index()):
            self._generalAccess.set_state(self.index(), True)
        self._timer.start()

    def stop_timer(self):
        self._timer.stop()
        self._generalAccess.set_state(self.index(), False)
        self.setData('00:00:00', QtCore.Qt.DisplayRole)

    def pause_timer(self):
        self._timer.stop()

    def _timer_timeout(self):
        self._count_down()
        # if time left is <= than 0
        if self.data(QtCore.Qt.DisplayRole).toTime() == QtCore.QTime(0, 0, 0, 0):
            self.stop_timer()
            self._generalAccess.set_state(self.index(), False)

    def timer_is_active(self):
        return self._timer.isActive()

    def time_span_is_zero(self):
        _is_zero = False
        if self.data(QtCore.Qt.DisplayRole).toTime() == QtCore.QTime(0, 0, 0, 0):
            _is_zero = True
        return _is_zero

    def _count_down(self):
        _timeLeft = self.data(QtCore.Qt.DisplayRole).toTime()
        _timeLeft = _timeLeft.addMSecs(-self._timer.interval())
        self.set_time(_timeLeft)

#     --------------------------------GeneralAccess------------------------------------------


class GeneralAccess(QtCore.QObject):
    @staticmethod
    def set_date_time_on(index, date_time_on):
        # Set new DateTime into 'Encendido' column
        index.model().itemFromIndex(index.parent().child(index.row(), 2)).set_date_time(date_time_on)

    @staticmethod
    def set_date_time_off(index, date_time_off):
        # Set new DateTime into 'Apagado' column
        index.model().itemFromIndex(index.parent().child(index.row(), 3)).set_date_time(date_time_off)

    @staticmethod
    def date_time_on_add_days(index, days):
        index.model().itemFromIndex(index.parent().child(index.row(), 2)).add_days(days)

    @staticmethod
    def date_time_off_add_days(index, days):
        index.model().itemFromIndex(index.parent().child(index.row(), 3)).add_days(days)

    @staticmethod
    def set_date_time_on_current_date(index):
        index.model().itemFromIndex(index.parent().child(index.row(), 2)).set_current_date()

    @staticmethod
    def set_date_time_off_current_date(index):
        index.model().itemFromIndex(index.parent().child(index.row(), 3)).set_current_date()

    @staticmethod
    def get_date_time_on(index):
        # Get DateTime from 'Encendido' column
        return index.model().itemFromIndex(index.parent().child(index.row(), 2)).get_date_time()

    @staticmethod
    def get_date_time_off(index):
        # Get DateTime from 'Apagado' column
        return index.model().itemFromIndex(index.parent().child(index.row(), 3)).get_date_time()

    @staticmethod
    def get_time_on(index):
        return index.model().itemFromIndex(index.parent().child(index.row(), 2)).get_time()

    @staticmethod
    def get_time_off(index):
        return index.model().itemFromIndex(index.parent().child(index.row(), 3)).get_time()

    @staticmethod
    def set_state(index, state):
        # Set State into 'Estado' column
        index.model().itemFromIndex(index.parent().child(index.row(), 5)).set_state(state)

    @staticmethod
    def state_is_on(index):
        # Get boolean value from 'Estado' column
        return index.model().itemFromIndex(index.parent().child(index.row(), 5)).is_on()