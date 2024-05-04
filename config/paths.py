from enum import Enum

class Paths(Enum):
    LEGAL_DATA = 'resource/'
    SAMPLE_RESOURCE = 'resource/sample_resource'
    DATA = '/path/to/data/'
    LOGS = '/path/to/logs/'
    IMAGES = '/path/to/images/'

# Example usage:
"""
config_path = Paths.CONFIG.value
data_path = Paths.DATA.value
logs_path = Paths.LOGS.value
"""
