

class SubProcess(metaclass=ABCMeta):
    def __init__(self, timeout):
        self.TimeOut = timeout
        self.TimeOutOffset = 0
        self.LastEvt = None
        self.LastEvtTime = 0
        self.History = None

    @property
    @abstractmethod
    def DefaultEvent(self):
        pass

    @property
    @abstractmethod
    def EndEvent(self):
        pass

    @property
    @abstractmethod
    def DeadEvent(self):
        pass

    def is_time_out(self, ti):
        return self.WaitUntil < ti

    @property
    def WaitUntil(self):
        return self.LastEvtTime + self.TimeOutOffset + self.TimeOut

    def progress(self, state, ti):
        if state is not self.LastEvt.Value:
            self.LastEvt = State(state, ti)
            self.History.append(self.LastEvt)
        self.LastEvtTime = ti

    def start(self):
        self.LastEvt = State(self.DefaultEvent, 0)
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
        if self.LastEvt.Value is not self.DefaultEvent:
            self.progress(self.DefaultEvent, self.WaitUntil)
            return True
        return False

    def end(self, ti):
        if self.is_time_out(ti):
            self.time_out()
        self.progress(self.EndEvent, ti)

    def die(self, ti):
        if self.is_time_out(ti):
            self.time_out()
        self.progress(self.DeadEvent, ti)

    def at(self, ti):
        evt = self.DefaultEvent
        for h in self.History:
            if h.Time <= ti:
                evt = h.Value
            else:
                break
        return evt
