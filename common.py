#!/usr/bin/env python3
from enum import IntEnum


class Modes(IntEnum):
    OVERWRITE = 0
    UPDATE = 1


SETTINGS: dict = {
    'output_dir': '',
    'mode': Modes.OVERWRITE
}
