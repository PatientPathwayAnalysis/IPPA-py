import pandas as pd
import os
import ippa
import tb
from tb.proc import RelatedIllness, Evaluation, Treatment


class ObsPseudo(ippa.Observation):
    def read_record(self, src, hos):
        self.Status = dict()
        self.Status['Patient_Cost'] = src.Patient_Cost
        self.Status['System_Cost'] = src.System_Cost
        self.Status['Visits'] = 1
        self.Status['Level'] = hos.Level

    def update_record(self, src, hos):
        self.Status['Patient_Cost'] += src.Patient_Cost
        self.Status['System_Cost'] += src.System_Cost
        self.Status['Visits'] += 1
        self.Status['Level'] = hos.Level


ctrl = tb.IPPA('TB')
ctrl.add_process('Pre', RelatedIllness(60))
ctrl.add_process('Eva', Evaluation(60))
ctrl.add_process('Tre', Treatment(30))
ctrl.set_observation(ObsPseudo())

ER = ctrl.EventReader
ER.define_disease('TB_DIAG')
ER.define_procedure('TB_PROC', {'L': list(range(0, 5)), 'H': list(range(5, 9))})
ER.define_drug('TB_DRUG', 'TB_DRUG_DAY', {'2nd': list(range(0, 5)), '1st': list(range(5, 8))})
ER.add_related_disease('CLD', 'CLD_DIAG')
ER.add_related_disease('ARD', 'RES_DIAG')
ER.add_related_disease('NTM', 'NTM_DIAG')


patients = pd.read_csv('../../Data/PseudoData/Input/IPPA_patients.csv', index_col=0)
ctrl.input_patients(patients, p_leave='OUT_DAY')


hospitals = pd.read_csv('../../Data/PseudoData/Input/IPPA_hospitals.csv', index_col=0)
ctrl.input_hospitals(hospitals, h_level='LEVEL')


records = pd.read_csv('../../Data/PseudoData/Input/IPPA_records.csv', index_col=0)
ctrl.input_records(records, 'ID', 'HOSP_ID', 'DAY')


ctrl.events2processes2episodes(read_end=3651)
ctrl.episodes2pathways()
ctrl.pathways2statistics()
ctrl.link_hospitals()


folder = 'E:/IPPA/Data/Output/Pseudo/'
if not os.path.exists(folder):
    os.makedirs(folder)

ctrl.results2json('{}{}'.format(folder, 'pathways.json'))
ctrl.statistics2csv('{}{}'.format(folder, 'pathways.csv'))
ctrl.hospital2csv('{}{}'.format(folder, 'hospital.csv'))
