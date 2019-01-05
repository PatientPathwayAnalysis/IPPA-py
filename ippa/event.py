from collections import namedtuple
import numpy as np


class Event:
    def __init__(self, tp, **kwargs):
        self.Type = tp
        self.Attributes = {k: v for k, v in kwargs.items() if v} if kwargs else None

    def __repr__(self):
        if self.Attributes:
            return '{}({} with {})'.format(
                type(self).__name__,
                self.Type,
                ', '.join(self.Attributes.keys()))
        else:
            return '{}({})'.format(type(self).__name__, self.Type)


class Disease(Event):
    @property
    def Procedures(self):
        try:
            return self.Attributes['procedures']
        except KeyError:
            return None

    @property
    def Drugs(self):
        try:
            return self.Attributes['drugs']
        except KeyError:
            return None


class RelatedDisease(Event):
    pass


class Comorbidity(Event):
    pass


class Drug:
    def __init__(self, types, amount):
        self.Types = [drug for drug in str(int(types))]
        self.Types.reverse()
        self.DrugDay = int(amount)

    @property
    def MainType(self):
        return np.argmax(self.Types) + 1

    @property
    def Strongest(self):
        return len(self.Types)

    def __repr__(self):
        return 'Drug(Types: {}, Amount: {} days)'.format(', '.join(self.Types), self.DrugDay)


class Procedure:
    def __init__(self, types):
        self.Types = [proc for proc in str(int(types))]
        self.Types.reverse()

    @property
    def Strongest(self):
        return len(self.Types)

    def __repr__(self):
        return 'Procedure(Types: ({}))'.format(', '.join(self.Types))


DefDiagnosis = namedtuple('DefDiagnosis', ('Type', 'Index'))
DefProcedure = namedtuple('DefProcedure', ('Type', 'Index'))
DefDrug = namedtuple('DefDrug', ('Type', 'Index', 'IndexAmount'))


class EventReader:
    def __init__(self, main_disease):
        self.MainDisease = main_disease
        self.Diagnosis = None
        self.Procedure = None
        self.Drug = None
        self.RelatedDiseases = dict()
        self.Comorbidities = dict()

    def define_disease(self, diagnosis):
        self.Diagnosis = DefDiagnosis(self.MainDisease, diagnosis)

    def define_procedure(self, procedure):
        self.Procedure = DefProcedure(self.MainDisease, procedure)

    def define_drug(self, drug_types, drug_amount):
        self.Drug = DefDrug(self.MainDisease, drug_types, drug_amount)

    def add_related_disease(self, tp, diagnosis):
        self.RelatedDiseases[tp] = DefDiagnosis(tp, diagnosis)

    def add_comorbidity(self, tp, diagnosis):
        self.Comorbidities[tp] = DefDiagnosis(tp, diagnosis)

    def read(self, record):
        events = dict()

        diag = record[self.Diagnosis.Index]
        diag = bool(diag)

        if self.Procedure:
            proc = record[self.Procedure.Index]
            proc = Procedure(proc) if proc else None
        else:
            proc = None

        drug = record[self.Drug.Index]
        drug = Drug(drug, record[self.Drug.IndexAmount]) if drug else None

        if diag or proc or drug:
            events['Main'] = Disease(self.MainDisease, procedures=proc, drugs=drug)

        rel = [RelatedDisease(k) for k, v in self.RelatedDiseases.items() if record[v.Index]]
        if rel:
            events['RelatedDz'] = rel

        com = [Comorbidity(k) for k, v in self.Comorbidities.items() if record[v.Index]]
        if com:
            events['Comorbidity'] = com

        return events
