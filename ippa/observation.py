from abc import ABCMeta, abstractmethod

__author__ = 'TimeWz667'


class Observation(metaclass=ABCMeta):
    def __init__(self):
        self.Status = None
        self.History = None
        self.LastTime = 0

    def initialise(self, rec, hos):
        self.LastTime = rec.Time
        self.Status = dict()
        self.read_record(rec.SourceData, hos)
        self.History = list()
        self.push_record()

    def update(self, rec, hos):
        self.LastTime = rec.Time
        self.update_record(rec.SourceData, hos)
        self.push_record()

    @abstractmethod
    def read_record(self, dat, hos):
        pass

    @abstractmethod
    def update_record(self, dat, hos):
        pass

    def push_record(self):
        self.Status['Time'] = self.LastTime
        self.History.append(dict(self.Status))

    def to_json(self):
        return self.History
