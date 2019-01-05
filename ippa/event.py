from collections import namedtuple
import operator
import numpy as np


class DigitSum:
    def __init__(self, gp):
        self.Groups = gp
        self.M = max([max(g) for g in gp.values()]) + 1

    def __call__(self, x):
        x = str(int(x)).zfill(self.M)
        return {k: sum(int(x[i]) for i in v) for k, v in self.Groups.items()}


class Event:
    def __init__(self, tp, **kwargs):
        self.Type = tp
        self.Attributes = {k: v for k, v in kwargs.items() if v} if kwargs else None

    def __getitem__(self, item):
        return self.Attributes[item]

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
        self.Types = types
        self.DrugDay = int(amount)
        self.DrugAmount = sum(types.values())

    @property
    def MainType(self):
        return max(self.Types.items(), key=operator.itemgetter(1))[0]

    def __repr__(self):
        return 'Drug(Types: {}, Amount: {}X{} days)'.format(', '.join(self.Types.keys()), self.DrugAmount, self.DrugDay)


class Procedure:
    def __init__(self, types):
        self.Types = types

    def __repr__(self):
        return 'Procedure(Types: ({}))'.format(', '.join(self.Types))


DefDiagnosis = namedtuple('DefDiagnosis', ('Type', 'Index'))
DefProcedure = namedtuple('DefProcedure', ('Type', 'Index', 'Groups'))
DefDrug = namedtuple('DefDrug', ('Type', 'Index', 'IndexAmount', 'Groups'))


class EventReader:
    def __init__(self, main_disease):
        self.MainDisease = main_disease
        self.Diagnosis = None
        self.Procedure = None
        self.ProcedureParser = None
        self.Drug = None
        self.DrugParser = None
        self.RelatedDiseases = dict()
        self.Comorbidities = dict()

    def define_disease(self, diagnosis):
        self.Diagnosis = DefDiagnosis(self.MainDisease, diagnosis)

    def define_procedure(self, procedure, proc_groups):
        self.Procedure = DefProcedure(self.MainDisease, procedure, proc_groups)
        self.ProcedureParser = DigitSum(proc_groups)

    def define_drug(self, drug_types, drug_amount, drug_groups):
        self.Drug = DefDrug(self.MainDisease, drug_types, drug_amount, drug_groups)
        self.DrugParser = DigitSum(drug_groups)

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
            proc = Procedure(self.ProcedureParser(proc)) if proc else None
        else:
            proc = None

        drug = record[self.Drug.Index]
        drug = Drug(self.DrugParser(drug), record[self.Drug.IndexAmount]) if drug else None

        if diag or proc or drug:
            events['Main'] = Disease(self.MainDisease, diag=diag, procedures=proc, drugs=drug)

        rel = [RelatedDisease(k) for k, v in self.RelatedDiseases.items() if record[v.Index]]
        if rel:
            events['RelatedDz'] = rel

        com = [Comorbidity(k) for k, v in self.Comorbidities.items() if record[v.Index]]
        if com:
            events['Comorbidity'] = com

        return events
