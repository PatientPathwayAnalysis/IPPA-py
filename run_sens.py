import pandas as pd
import os
import tb
from tb.proc import RelatedIllness, Evaluation, Treatment


ctrl = tb.IPPA('TB')

ER = ctrl.EventReader
ER.define_disease('TB_DIAG')
ER.define_procedure('TB_PROC', {'L': list(range(0, 5)), 'H': list(range(5, 9))})
ER.define_drug('TB_DRUG', 'TB_DRUG_DAY', {'2nd': list(range(0, 5)), '1st': list(range(5, 8))})
ER.add_related_disease('CLD', 'CLD')
ER.add_related_disease('ARD', 'ARD')
ER.add_related_disease('NTM', 'NTM')
ER.add_comorbidity('CLD', 'CLD')
ER.add_comorbidity('DM', 'DM')
ER.add_comorbidity('HIV', 'HIV')


patients = pd.read_csv('../../Data/Input/Reformed/patients.csv', index_col=0)
p_map = {p: "P{:04d}".format(i) for i, p in enumerate(set(patients.ID), 1)}
patients.ID = [p_map[i] for i in patients.ID]
# patients = pd.read_csv('../../Data/PseudoData/Input/IPPA_patients.csv', index_col=0)
ctrl.input_patients(patients, p_leave='Out', by_year='Year')


hospitals = pd.read_csv('../../Data/Input/Reformed/hospitals.csv', index_col=0)
h_map = {h: "H{:05d}".format(i) for i, h in enumerate(hospitals.HOSP_ID, 1)}
hospitals.HOSP_ID = [h_map[i] for i in hospitals.HOSP_ID]
# hospitals = pd.read_csv('../../Data/PseudoData/Input/IPPA_hospitals.csv', index_col=0)
ctrl.input_hospitals(hospitals)

records = [pd.read_csv('../../Data/Input/Reformed/records{}.csv'.format(yr), index_col=0) for yr in range(2001, 2011)]
records = pd.concat(records)
records.ID = [p_map[i] for i in records.ID]
records.HOSP_ID = [h_map[i] for i in records.HOSP_ID]

records = records.sort_values(['ID', 'DAY'])
records = records.reset_index()
records = records.drop(columns='index')
# records = pd.read_csv('../../Data/PseudoData/Input/IPPA_records.csv', index_col=0)

ctrl.input_records(records, 'ID', 'HOSP_ID', 'DAY')


for tp in [30, 60, 90, 120]:
    for te in [30, 60, 90, 120]:
        print("S", tp, te)
        ctrl.Processes.clear()
        ctrl.add_process('Pre', RelatedIllness(tp))
        ctrl.add_process('Eva', Evaluation(te))
        ctrl.add_process('Tre', Treatment(30))
        ctrl.events2processes2episodes(read_end=3651)
        ctrl.episodes2pathways()
        ctrl.pathways2statistics()
        ctrl.clear_hospitals()
        ctrl.link_hospitals()

        folder = 'E:/IPPA/Data/Output/IPPA_3SP/Sens/SC{}_{}_30/'.format(tp, te)
        if not os.path.exists(folder):
            os.makedirs(folder)

        ctrl.results2json('{}{}'.format(folder, 'pathways.json'))
        ctrl.statistics2csv('{}{}'.format(folder, 'pathways.csv'))
        ctrl.hospital2csv('{}{}'.format(folder, 'hospitals.csv'))
