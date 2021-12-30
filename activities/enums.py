from enum import Enum


class PropertyStatus(Enum):

    enabled = 'enabled'
    disabled = 'disabled'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class ActivityStatus(Enum):

    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
