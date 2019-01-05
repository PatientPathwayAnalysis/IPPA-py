__author__ = "TimeWz667"


class Record:
    def __init__(self, pid, hid, t, src, evt):
        self.Patient = pid
        self.Hospital = hid
        self.Time = t
        self.SourceData = src
        self.Events = evt

    def __repr__(self):
        return 'Record(Patient={}, Hospital={}, Day={}, Events={})'.format(self.Patient, self.Hospital, self.Time,
                                                                           self.Events)
