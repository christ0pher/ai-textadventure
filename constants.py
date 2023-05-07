from enum import Enum


class GamestatusEnum(Enum):
    INIT = 0
    STARTED = 1
    FINISHED = 2
    PREPARE_STORY = 3