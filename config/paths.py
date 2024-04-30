from enum import Enum

class Paths(Enum):
    CONFIG = '/path/to/config/'
    DATA = '/path/to/data/'
    LOGS = '/path/to/logs/'
    IMAGES = '/path/to/images/'

# Example usage:
"""
config_path = Paths.CONFIG.value
data_path = Paths.DATA.value
logs_path = Paths.LOGS.value
"""
