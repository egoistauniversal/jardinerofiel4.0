from PyQt4 import QtCore


class Options(QtCore.QObject):

    @staticmethod
    def get_component_name(option):
        return {1: 'Reloj',
                2: 'Temporizador',
                3: 'Pulsador'}[option]

    @staticmethod
    def get_component_type(option):
        return {1: 'Reloj',
                2: 'Temporizador',
                3: 'Pulsador'}[option]

    @staticmethod
    def get_sensor_name(option):
        return {1: 'Temperatura (DS18B20)',
                2: 'Temperatura y Humedad (DHT11)',
                4: 'PH',
                5: 'EC'}[option]

    @staticmethod
    def get_sensor_type(option):
        return {1: 'Temperatura (DS18B20)',
                2: 'Temperatura (DHT11)',
                3: 'Humedad (DHT11)',
                4: 'PH',
                5: 'EC'}[option]

    @staticmethod
    def get_control_name(option):
        return {1: 'Sensor',
                2: 'Componentes'}[option]