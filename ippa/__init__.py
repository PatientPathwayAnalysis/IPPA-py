from .patient import patients_from_data_frame, patients_from_json
from .hospital import hospitals_from_data_frame, hospitals_from_json
from .event import EventReader
from .record import Record
from .process import Process


class IPPA:
    def __init__(self, title):
        self.Patients = None
        self.P_ID = None
        self.Hospitals = None
        self.H_ID = None
        self.DfRecords = None
        self.IndRecords = None
        self.EventReader = EventReader(title)

    def input_patients(self, patients, p_id='ID', p_leave='OUT_DAY', p_attributes=None, by_year=False):
        ps = patients_from_data_frame(patients,
                                      p_id=p_id, p_leave=p_leave, p_attributes=p_attributes, by_year=by_year)

        self.Patients = {p.ID: p for p in ps}
        self.P_ID = [p.ID for p in ps]
        print('{} patients inputted'.format(len(self.P_ID)))

    def input_hospitals(self, hospitals, h_id='HOSP_ID', h_level='Level', h_attributes=None):
        hs = hospitals_from_data_frame(hospitals, h_id=h_id, h_level=h_level, h_attributes=h_attributes)

        self.Hospitals = {h.ID: h for h in hs}
        self.H_ID = [h.ID for h in hs]
        print('{} hospital inputted'.format(len(self.H_ID)))

    def input_records(self, records, p_id, h_id, day):
        self.DfRecords = records.groupby(p_id)
        self.IndRecords = p_id, h_id, day
        print('{} health care records inputted'.format(records.shape[0]))

    def get_patient(self, i):
        if not isinstance(i, str):
            i = self.P_ID[i]
        p = self.Patients[i]
        if p.Records:
            return p

        recs = self.DfRecords.get_group(p.ID)

        col = list()
        for _, rec in recs.iterrows():
            evt = self.EventReader.read(rec)
            if evt:
                col.append(Record(rec[self.IndRecords[0]], rec[self.IndRecords[1]], rec[self.IndRecords[2]],
                                  rec, evt))
        p.Records = col
        return p

    def get_hospital(self, i):
        if not isinstance(i, str):
            i = self.H_ID[i]
        return self.Hospitals[i]

    def define_ordered_event(self, tp, fn):
        pass

    def add_process(self, name, sp):
        pass

    def define_episode_filter(self, fn):
        pass

    def define_pathway_fn(self, fn):
        pass

    def define_statistics_fn(self, fn):
        pass

    def records2events(self):
        pass

    def events2processes(self, time_outs):
        pass

    def processes2episodes(self):
        pass

    def episodes2pathways(self):
        pass

    def pathways2statistics(self):
        pass

    def results2json(self, file_path):
        pass

    def statistics2csv(self, file_path):
        pass

    def hospital2csv(self, file_path):
        pass

    def run_all(self, time_outs, res_json, stats_csv, hosp_csv):
        self.records2events()
        self.events2processes(time_outs)
        self.processes2episodes()
        self.episodes2pathways()
        self.pathways2statistics()
        self.results2json(res_json)
        self.statistics2csv(stats_csv)
        self.hospital2csv(hosp_csv)
