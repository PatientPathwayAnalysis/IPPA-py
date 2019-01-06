__author__ = 'TimeWz667'


class Episode:
    def __init__(self, i, history, recs):
        self.PatientID = i
        self.Attributes = dict()
        self.History = history
        self.Records = recs
        self.Anchors = None
        self.Pathway = None
        self.Observations = None
        self.TimeFrame = (history[0]['Time'], history[-1]['Time'])

    def __getitem__(self, item):
        return self.Attributes[item]

    def __setitem__(self, key, value):
        self.Attributes[key] = value

    def to_json(self):
        hist = list()
        for his in self.History:
            hist.append({k: (v.name if k is not 'Time' else v) for k, v in his.items()})

        return {
            'ID': self.PatientID,
            'Attributes': self.Attributes,
            'History': hist,
            'Observations': self.Observations.to_json(),
            'Pathway': [{'Time': pa['Time'], 'Stage': pa['Stage'].name} for pa in self.Pathway]
        }

    def to_data(self):
        dat = dict()
        dat['ID'] = self.PatientID
        dat.update(self.Attributes)
        return dat
