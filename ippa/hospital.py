from collections import Counter

__author__ = "TimeWz667"


class Hospital:
    def __init__(self, i, lv, attributes):
        """
        Hospital entity
        :param i: id, relevant to hid in records
        :param lv: hospital level
        :type lv: int | str
        :param attributes: attributes to be attached to pathways
        :type attributes: dict
        """
        self.ID = i
        self.Level = lv
        self.Attributes = dict(attributes)
        self.Counts = Counter()

    def __getitem__(self, item):
        return self.Counts[item]

    def count(self, event='Visit'):
        """
        Add a count on an event
        :param event: event to count
        :type: str
        """
        self.Counts[event] += 1

    def to_json(self):
        return {
            'HID': self.ID,
            'Level': self.Level,
            'Attributes': self.Attributes,
            'Counts': dict(self.Counts)
        }

    def to_data(self):
        dat = {'HID': self.ID, 'Level': self.Level}
        dat.update(self.Attributes)
        dat.update(self.Counts)
        return dat

    def __repr__(self):
        return 'Hospital {} in Level {}'.format(self.ID, self.Level)


def hospitals_from_data_frame(hospitals, h_id='HOSP_ID', h_level='Level', h_attributes=None):
    """
    Read hospitals from a pandas DataFrame
    :param hospitals: DataFrame of hospitals
    :param h_id: index of hospital id
    :param h_level: index of hospital level
    :param h_attributes: indices of hospitals' attributes
    :return: hospital entities
    :rtype: list
    """
    if h_attributes:
        h_attributes = [atr for atr in h_attributes if atr in hospitals.columns]
    else:
        h_attributes = [atr for atr in hospitals.columns if atr not in [h_id, h_level]]

    return [Hospital(h[h_id], h[h_level], h[h_attributes]) for _, h in hospitals.iterrows()]


def hospitals_from_json(hospitals, h_id='HOSP_ID', h_level='Level', h_attributes=None):
    # todo
    pass
