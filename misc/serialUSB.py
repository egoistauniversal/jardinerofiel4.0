from PyQt4 import QtCore
import serial
import struct
import time


class PayLoad(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self._tab = None
        self._device_type = None
        self._pin = None
        self._state = None

    def set(self, tab, device_type, pin, state):
        self._tab = tab
        self._device_type = device_type
        self._pin = pin
        self._state = state

    def get_tab(self):
        return self._tab

    def get_device_type(self):
        return self._device_type

    def get_pin(self):
        return self._pin

    def get_state(self):
        return self._state


class SerialUSB(QtCore.QObject):
    def __init__(self, browser):
        QtCore.QObject.__init__(self)
        self._browser = browser
        self._port = '/dev/ttyUSB0'
        self._bauds = '57600'
        self._timeout = 0
        self._mySerial = None
        self.error = False
        self._detect_serial_connection()
        self._payload = PayLoad()
        self._header = 'H'
        self._footer = 'F'

    def _detect_serial_connection(self):
        try:
            self._mySerial = serial.Serial(self._port, self._bauds, timeout=self._timeout)
            time.sleep(2)
            self._mySerial.flushInput()
            self._browser.print_normal_message('Connexion correcta con el arduino en ' + self._port)

        except Exception, e:
            self.error = True
            self._browser.print_alert_message(str(e) + ' - Error al conectar con el arduino')

    def write(self, tab, device_type, pin, state):
        self._payload.set(tab, device_type, pin, state)
        self._mySerial.write(
            struct.pack('cbbbbbc', self._header, 1, self._payload.get_tab(), self._payload.get_device_type(),
                        self._payload.get_pin(), self._payload.get_state(), self._footer))

    def read(self):
        _data = []
        # Read serial data from Arduino
        while len(_data) == 0:
            _data = self._mySerial.readlines()
        _value = _data[0].strip()
        # print _data
        return _value

    def close(self):
        if not self.error:
            self._mySerial.close()

