import ippa


class TB3Obs(ippa.Observation):
    def read_record(self, src, hos):
        self.Status = dict()
        self.Status['Patient_Cost'] = src.Patient_Cost
        self.Status['System_Cost'] = src.System_Cost
        self.Status['Visits'] = 1
        self.Status['Level'] = hos.Level
        self.Status['Sector'] = src.Sector
        self.Status['InOut'] = src.InOut

    def update_record(self, src, hos):
        self.Status['Patient_Cost'] += src.Patient_Cost
        self.Status['System_Cost'] += src.System_Cost
        self.Status['Visits'] += 1
        self.Status['Level'] = hos.Level
        self.Status['Sector'] = src.Sector
        self.Status['InOut'] = src.InOut
