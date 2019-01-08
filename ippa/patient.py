__author__ = "TimeWz667"


class Patient:
    def __init__(self, i, leave, attributes):
        """
        Patient entity
        :param i: id of a patient relevant to id in records
        :param leave: day of leaving the system
        :type leave: int
        :param attributes: attributes to be attached to pathways
        :type attributes: dict
        """
        self.ID = i
        try:
            self.LeavingDay = float(leave)
        except AttributeError:
            self.LeavingDay = float('Inf')

        self.Attributes = dict(attributes)
        self.Records = list()
        self.Episodes = dict()

    def leaving_day(self):
        return self.LeavingDay

    def to_json(self):
        """
        to a json formatted dict
        :return: a dict which can be output as json
        """
        return {
            'ID': self.ID,
            'OutDay': self.LeavingDay,
            'Attributes': self.Attributes
        }

    def to_data(self):
        """
        to a data entry
        :return: a dict without nested structure
        """
        dat = {'ID': self.ID, 'OutDay': self.LeavingDay}
        dat.update(self.Attributes)
        return dat

    def __repr__(self):
        return 'Patient {} with {} records, {} pathways'.format(self.ID, len(self.Records), len(self.Episodes))


class PatientByYear(Patient):
    def __init__(self, i, leave, attributes):
        Patient.__init__(self, i, leave, attributes)
        self.Year = list(attributes.keys())[0]

    def to_json(self):
        """
        to a json formatted dict
        :return: a dict which can be output as json
        """
        return {
            'ID': self.ID,
            'OutDay': self.LeavingDay,
            'Attributes': self.Attributes[self.Year]
        }

    def to_data(self):
        """
        to a data entry
        :return: a dict without nested structure
        """
        dat = {'ID': self.ID, 'OutDay': self.LeavingDay, 'Year': self.Year}
        dat.update(self.Attributes[self.Year])
        return dat

    def to_data_in_year(self, yr):
        """
        to a data entry in a specific year
        :param yr: year
        :return: a dict without nested structure
        """
        dat = {'ID': self.ID, 'OutDay': self.LeavingDay, 'Year': yr}
        dat.update(self.Attributes[yr])
        return dat


def patients_from_data_frame(patients, p_id='ID', p_leave='OUT_DAY', p_attributes=None, by_year=False):
    """
    Read patients from a pandas DataFrame
    :param patients: DataFrame of patients
    :param p_id: index of patient id
    :param p_leave: index of patient's leaving day
    :param p_attributes: indices of patients' attributes
    :param by_year: false for constant patient background, index of year for dynamic patient background
    :return: patient entities
    :rtype: list
    """
    if not by_year:
        if p_attributes:
            p_attributes = [atr for atr in p_attributes if atr in patients.columns]
        else:
            p_attributes = [atr for atr in patients.columns if atr not in [p_id, p_leave]]
        return [Patient(p[p_id], p[p_leave], p[p_attributes]) for _, p in patients.iterrows()]
    else:
        if p_attributes:
            p_attributes = [atr for atr in p_attributes if atr in patients.columns]
        else:
            p_attributes = [atr for atr in patients.columns if atr not in [p_id, p_leave, by_year]]
        pg = patients.groupby(p_id)
        ids = list(pg.groups.keys())
        ps = list()
        for i in ids:
            d = pg.get_group(i)
            d = PatientByYear(i, d.iloc[1, ][p_leave], {r[by_year]: r[p_attributes] for _, r in d.iterrows()})
            ps.append(d)
        return ps


def patients_from_json(patients, p_id='ID', p_leave='OUT_DAY', p_attributes=None):
    # todo
    pass
