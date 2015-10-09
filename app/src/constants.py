from enum import Enum


class Template_Score(Enum):
    perfect_match = 0
    not_matching = 1
    unsure = 2


class Nginx_Dir_Type(Enum):
    light = 0
    full = 1


class Config_Status(Enum):
    enabled = 0
    disabled = 1
    not_found = 2


class Template_Type(Enum):
    managed = 0
    unmanaged = 1
    constant = 2
