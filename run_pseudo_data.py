import pandas as pd
import os
import tb


# Initialise a new IPPA
ctrl = tb.IPPA('TB', tor=60, toe=60, tot=30)


# Set the definition of events
ER = ctrl.EventReader
ER.define_disease('TB_DIAG')
ER.define_procedure('TB_PROC', {'L': list(range(0, 5)), 'H': list(range(5, 9))})
ER.define_drug('TB_DRUG', 'TB_DRUG_DAY', {'2nd': list(range(0, 5)), '1st': list(range(5, 8))})
ER.add_related_disease('CLD', 'CLD_DIAG')
ER.add_related_disease('ARD', 'RES_DIAG')
ER.add_related_disease('NTM', 'NTM_DIAG')


# Set input folder
folder_i = '../../Data/PseudoData/Input/'

# Read patient data
patients = pd.read_csv(folder_i + 'IPPA_patients.csv', index_col=0)
ctrl.input_patients(patients, p_leave='OUT_DAY')


# Read hospital data
hospitals = pd.read_csv(folder_i + 'IPPA_hospitals.csv', index_col=0)
ctrl.input_hospitals(hospitals, h_level='LEVEL')


# Read healthcare records
records = pd.read_csv(folder_i + 'IPPA_records.csv', index_col=0)
ctrl.input_records(records, 'ID', 'HOSP_ID', 'DAY')


# Run the analysis
ctrl.events2processes2episodes(read_end=3651)
ctrl.episodes2pathways()
ctrl.pathways2statistics()
ctrl.link_hospitals()


folder_o = "../../Data/Output/Pseudo/"

if not os.path.exists(folder_o):
    os.makedirs(folder_o)

ctrl.results2json(folder_o + 'pathways.json')
ctrl.statistics2csv(folder_o + 'pathways.csv')
ctrl.hospital2csv(folder_o + 'hospital.csv')
