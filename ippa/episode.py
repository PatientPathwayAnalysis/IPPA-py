__author__ = 'TimeWz667'


class Episode:
    def __init__(self, i, history, recs):
        self.PatientID = i
        self.Anchors = None
        self.Background = None
        self.History = history
        self.Observations = None
        self.Pathway = None
        self.Statistics = None
        self.Records = recs
        self.TimeFrame = (history[0]['Time'], history[-1]['Time'])

    def reform_background(self, reform_cov):
        self.Background.reform_cov(reform_cov)

    def to_json(self):
        hist = list()
        for his in self.History:
            hist.append({k: (v.name if k is not 'Time' else v) for k, v in his.items()})

        return {
            'ID': self.PatientID,
            'Background': self.Background.to_json(),
            'History': hist,
            'Observations': self.Observations.to_json(),
            'Pathway': [{'Time': pa['Time'], 'Stage': pa['Stage'].name} for pa in self.Pathway],
            'Statistics': self.Statistics
        }

    def to_data(self):
        dat = dict()
        dat['ID'] = self.PatientID
        dat.update(self.Statistics)
        dat.update(self.Background.to_json())
        return dat
