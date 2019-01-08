from enum import Enum, auto


class TBStage(Enum):
    NONE = auto()
    WAITING = auto()
    EVALUATING_L = auto()
    EVALUATING_H = auto()
    # EVALUATING_E = auto()
    IE = auto()
    REEVALUATING_L = auto()
    REEVALUATING_H = auto()
    #REEVALUATING_E = auto()
    TREATING_F = auto()
    TC = auto()
    TREATING_S = auto()
    LOST = auto()
    CENSORED = auto()
    COMPLETED = auto()
    DEAD = auto()
