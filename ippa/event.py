class Event:
    def __init__(self, tp, **kwargs):
        self.Type = tp
        self.Attributes = dict(kwargs) if kwargs else None

    def __repr__(self):
        if self.Attributes:
            return '{} with [{}]'.format(
                self.Type,
                ', '.join(self.Attributes.keys()))
        else:
            return self.Type
