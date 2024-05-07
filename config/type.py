from enum import Enum

class DocType(Enum):
    LEGAL_DATA = 'resource/'
    SAMPLE_RESOURCE = 'resource/sample_resource'
    DATA = '/path/to/data/'
    LOGS = '/path/to/logs/'
    IMAGES = '/path/to/images/'