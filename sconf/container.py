class DictContainer:
    """ Dictionary container """

    def __init__(self, data=None):
        self.data = data or {}

    def get(self, *args, **kwargs):
        return self.data.get(*args, **kwargs)

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return repr(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __contains__(self, key):
        return key in self.data

    def __len__(self):
        return len(self.data)

    def __eq__(self, other):
        return self.data == other

    def items(self):
        return self.data.items()

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()
