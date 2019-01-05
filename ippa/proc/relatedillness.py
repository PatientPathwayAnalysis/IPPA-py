from ippa import Process


class RelatedIllness(Process):
    def find_new_state(self, events, ti):
        if 'RelatedDz' in events:
            return events['RelatedDz'][0].Type
        else:
            return False
