
from enum import Enum

class SupportedDevices(Enum):
    RAZOR = 'SparkFunRazor'
    SEEED = 'SeeedXIAO'

class SerialRef(Enum):
    SERIAL = 'Serial'
    DEVICE = 'device'
    PORT = 'port'
    BOUNDRATE = 'boundrate'
    BOOT_TIME = 'boot_time'

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

class EncodingFormat(Enum):
    UTF_8 = "utf-8"