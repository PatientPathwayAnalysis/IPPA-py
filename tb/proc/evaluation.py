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
                if proc.Types['H'] > 0 or self.LastEvt.Value == 'Strong':
                    return 'Strong'
                else:
                    return 'Weak'
        except KeyError:
            return False
        return False
