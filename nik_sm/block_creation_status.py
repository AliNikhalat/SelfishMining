from enum import Enum


class BlockCreationStatus(Enum):
    EndTow = 1,
    EndTimeWindow = 2,
    Normal = 3
