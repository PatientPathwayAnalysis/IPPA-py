from abc import ABCMeta, abstractmethod
from collections import namedtuple

__author__ = 'TimeWz667'


State = namedtuple('State', ('Value', 'Time'))


class Process(metaclass=ABCMeta):
    def __init__(self, timeout):
        self.TimeOut = timeout
        self.TimeOutOffset = 0
        self.LastEvt = None
        self.LastEvtTime = 0
        self.History = None

    @property
    def DefaultState(self):
        return 'None'

    @property
    def EndState(self):
        return 'Lost'

    @property
    def DeadState(self):
        return 'Dead'

    def is_time_out(self, ti):
        return self.WaitUntil < ti

    @property
    def WaitUntil(self):
        return self.LastEvtTime + self.TimeOutOffset + self.TimeOut

    def progress(self, state, ti):
        if state != self.LastEvt.Value:
            self.LastEvt = State(state, ti)
            self.History.append(self.LastEvt)
        self.LastEvtTime = ti

    def start(self):
        self.LastEvt = State(self.DefaultState, 0)
        self.History = [self.LastEvt]
        self.LastEvtTime = 0

    def update(self, events, ti):
        if self.is_time_out(ti):
            self.time_out()
        st = self.find_new_state(events, ti)
        if st:
            self.progress(st, ti)
            return True
        return False

    @abstractmethod
    def find_new_state(self, events, ti):
        """
        find the upcoming state
        :param events: events
        :type events: dict
        :param ti: current time
        :return: return new state if possible else False
        """
        pass

    def time_out(self):
        if self.LastEvt.Value != self.DefaultState:
            self.progress(self.DefaultState, self.WaitUntil)
            return True
        return False

    def end(self, ti):
        if self.is_time_out(ti):
            self.time_out()
        self.progress(self.EndState, ti)

    def die(self, ti):
        if self.is_time_out(ti):
            self.time_out()
        self.progress(self.DeadState, ti)

    def at(self, ti):
        evt = self.DefaultState
        for h in self.History:
            if h.Time <= ti:
                evt = h.Value
            else:
                break
        return evt
