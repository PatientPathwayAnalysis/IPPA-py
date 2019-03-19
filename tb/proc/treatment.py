from ippa import Process


class Treatment(Process):
    def __init__(self, to):
        Process.__init__(self, to)
        self.CurrentDrug = None
        self.DrugDayEnd = 0
        self.DrugDayStart = 0

    def start(self):
        Process.start(self)
        self.CurrentDrug = None
        self.DrugDayEnd = 0
        self.DrugDayStart = 0

    def find_new_state(self, events, ti):
        try:
            evt = events['Main']
            drug = evt.Drugs
            if not drug:
                return False

            self.use_drug(drug, ti)

            if drug.DrugDay >= 7 and drug.DrugAmount >= 2:
                if drug.MainType == '2nd':
                    # self.use_drug(drug, ti)
                    return '2nd'
                else:
                    if self.LastEvt.Value != '2nd':
                        # self.use_drug(drug, ti)
                        return '1st'
                    else:
                        return '2nd'
            elif self.LastEvt.Value not in ['1st', '2nd']:
                # self.use_drug(drug, ti)
                return 'Empirical'
        except KeyError:
            return False
        return False

    def use_drug(self, drug, ti):
        if self.CurrentDrug in ['2nd', drug.MainType]:
            if self.DrugDayEnd < ti:
                self.DrugDayEnd = ti + drug.DrugDay
            else:
                self.DrugDayEnd = self.DrugDayEnd + drug.DrugDay
            self.TimeOutOffset = self.DrugDayEnd - ti
        else:
            self.CurrentDrug = drug.MainType
            self.DrugDayStart = ti
            self.DrugDayEnd = ti + drug.DrugDay
            self.TimeOutOffset = drug.DrugDay

    def time_out(self):
        if self.LastEvt.Value is not self.DefaultState:
            if self.CurrentDrug:
                self.progress(self.DefaultState, self.DrugDayEnd)
            else:
                self.progress(self.DefaultState, self.WaitUntil)
            self.CurrentDrug = None
            return True
        return False
