from abc import ABCMeta, abstractmethod

__author__ = 'TimeWz667'


class Observation(metaclass=ABCMeta):
    def __init__(self):
        self.Status = None
        self.History = None
        self.LastTime = 0

    def initialise(self, rec):
        self.LastTime = rec.Time
        self.Status = dict()
        self.read_record(rec)
        self.History = list()
        self.push_record()

    def update(self, rec):
        self.LastTime = rec.Time
        self.update_record(rec)
        self.push_record()

    @abstractmethod
    def read_record(self, rec):
        pass

    @abstractmethod
    def update_record(self, rec):
        pass

    def push_record(self):
        self.Status['Time'] = self.LastTime
        self.History.append(dict(self.Status))

    def to_json(self):
        return self.History


def read_observations(episode, obs):
    recs = episode.Records
    obs.initialise(recs[0])
    for rec in recs[1:]:
        obs.update(rec)
    return obs
