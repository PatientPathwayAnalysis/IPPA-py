import ippa
from tb.stages import TBStage
from tb.proc import Evaluation, Treatment
from tb.observation import TB3Obs
from tb.fn import *
from tb.post import *


class IPPA(ippa.IPPA):
    def __init__(self, name):
        ippa.IPPA.__init__(self, name)

        self.define_episode_filter(is_eligible)
        self.define_anchor_fn(identify_critical_stages)
        self.define_pathway_fn(form_pathway)
        self.set_observation(TB3Obs())
        self.define_statistics_fn(summary)
        self.define_event_count(count_event)

