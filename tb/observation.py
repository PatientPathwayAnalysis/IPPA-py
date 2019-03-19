import ippa


class TB3Obs(ippa.Observation):
    def __init__(self):
        ippa.Observation.__init__(self)
        self.HospitalSector = False

    def read_record(self, src, hos):
        self.Status = dict()
        self.Status['Patient_Cost'] = src.Patient_Cost
        self.Status['System_Cost'] = src.System_Cost
        self.Status['Visits'] = 1
        self.Status['Level'] = hos.Level
        try:
            self.Status['Sector'] = src.Sector
            self.Status['InOut'] = src.InOut
        except AttributeError:
            self.HospitalSector = False
        else:
            self.HospitalSector = True

    def update_record(self, src, hos):
        self.Status['Patient_Cost'] += src.Patient_Cost
        self.Status['System_Cost'] += src.System_Cost
        self.Status['Visits'] += 1
        self.Status['Level'] = hos.Level
        if self.HospitalSector:
            self.Status['Sector'] = src.Sector
            self.Status['InOut'] = src.InOut
