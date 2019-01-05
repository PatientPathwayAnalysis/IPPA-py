from .patient import *
from .hospital import *
from .event import *


class IPPA:
    def __init__(self):
        pass

    def load_patients(self, file_path):
        pass

    def load_hospitals(self, file_path):
        pass

    def load_records(self, file_path):
        pass

    def define_event(self, tp, fn):
        pass

    def define_ordered_event(self, tp, fn):
        pass

    def add_sub_process(self, name, sp):
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
