import ippa
from tb.stages import TBStage
from tb.proc import Evaluation, Treatment, RelatedIllness
from tb.observation import TB3Obs
from tb.fn import *
from tb.post import *


class IPPA(ippa.IPPA):
    def __init__(self, name, tor=60, toe=60, tot=30):
        """
        A controller for implementing the IPPA
        :param name: identity of this analysis
        :param tor: time-out of Related illness
        :param toe: time-out of Evaluation
        :param tot: time-out of Treatment (After the end of the last prescription)
        """
        assert tor > 1
        assert toe > 1
        assert tot > 1
        ippa.IPPA.__init__(self, name)
        self.define_episode_filter(is_eligible_episode)
        self.define_anchor_fn(identify_critical_stages)
        self.define_pathway_fn(form_pathway)
        self.define_pathway_filter(is_eligible_pathway)
        self.set_observation(TB3Obs())
        self.define_statistics_fn(summary)
        self.define_event_count(count_event)
        self.ArrivalTiming = find_arrival_timing
        self.add_process('Pre', RelatedIllness(tor))
        self.add_process('Eva', Evaluation(toe))
        self.add_process('Tre', Treatment(tot))

    def link_hospitals(self):
        ippa.IPPA.link_hospitals(self)
        for i in self.P_ID:
            p = self.get_patient(i)
            for epi in p.Episodes:
                self.ArrivalTiming(self, epi)
