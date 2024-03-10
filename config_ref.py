
from enum import Enum

class SerialRef(Enum):
    SERIAL = 'Serial'
    DEVICE = 'device'
    PORT = 'port'
    BOUNDRATE = 'boundrate'
    BOOT_TIME = 'boot_time'

class SerialCmd(Enum):
    READ = 'r'
    WRITE = 'w'
    EXECUTE = 'x'

class UnitRef(Enum):
    UNITS = 'Units'
    ORIN_SCALE = 'orin_scale'
    ACEL_SCALE = 'acel_scale'
    GYRO_SCALE = 'gyro_scale'

class GeneralCmdRef(Enum):
    START_POST = '#o1'
    STOP_POST = '#o0'
    OUTPUT_FORMAT = '#ox'

class CalibRef(Enum):
    CALIB = 'Calib'
    VAL = 'Val'
    CMD = 'Cmd'

class YAPRGRef(Enum):
    HEAD_SEP = '='
    ELEM_SEP = ','
    ORIN_X = 0
    ORIN_Y = 1
    ORIN_Z = 2
    ACEL_X = 3
    ACEL_Y = 4
    ACEL_Z = 5
    GYRO_X = 6
    GYRO_Y = 7
    GYRO_Z = 8

class AxisRef(Enum):
    X = 'x'
    Y = 'y'
    Z = 'z'

class EncodingFormat(Enum):
    UTF_8 = "utf-8"