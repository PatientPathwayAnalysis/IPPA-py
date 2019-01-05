from ippa import Process


# todo evaluation with ranking

class Evaluation(Process):
    def find_new_state(self, events, ti):
        try:
            evt = events['Main']
            proc = evt.Procedures
            if evt['diag']:
                return 'Strong'
            elif proc:
                if proc['H'] > 0:
                    return 'Strong'
                elif self.LastEvt.Value in ['None', 'Weak']:
                    return 'Weak'
                else:
                    return 'Strong'
        except KeyError:
            return False
        return False
