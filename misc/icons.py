from PyQt4 import QtCore, QtGui


class Icons(QtCore.QObject):

    @staticmethod
    def get_component_icon(c_type):
        _iconList = ['images/standardItems/componentTypes/clock.png',
                     'images/standardItems/componentTypes/timer.png',
                     'images/standardItems/componentTypes/semiTimer.png']
        return QtGui.QIcon(_iconList[c_type - 1])

    @staticmethod
    def get_sensor_icon(c_type):
        _iconList = ['images/standardItems/sensorTypes/thermometer01.jpeg',
                     'images/standardItems/sensorTypes/thermometer02.png',
                     'images/standardItems/sensorTypes/humidity.jpeg',
                     'images/standardItems/sensorTypes/ph.jpg',
                     'images/standardItems/sensorTypes/ec.jpeg']
        return QtGui.QIcon(_iconList[c_type - 1])

    @staticmethod
    def get_control_icon(c_type):
        _iconList = ['images/standardItems/controlTypes/sensorTypes.png',
                     'images/standardItems/controlTypes/componentTypes.png']
        return QtGui.QIcon(_iconList[c_type - 1])

    @staticmethod
    def get_state_icon(state):
        _iconList = ['images/standardItems/state/off.png',
                     'images/standardItems/state/on.png']
        if state:
            return QtGui.QIcon(_iconList[1])
        else:
            return QtGui.QIcon(_iconList[0])

    @staticmethod
    def get_active_icon(active):
        _iconList = ['images/standardItems/active/deactive.png',
                     'images/standardItems/active/active.png']
        if active:
            return QtGui.QIcon(_iconList[1])
        else:
            return QtGui.QIcon(_iconList[0])