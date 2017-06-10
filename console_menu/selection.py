class Selection(object):
    def __init__(self, label, value=None):
        self.label = str(label)
        self.value = value if value is not None else label

    def __repr__(self):
        return 'Selection(%s)' % self.label