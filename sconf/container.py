class DictContainer:
    """ Dictionary container """

    def __init__(self, data=None):
        self._data = data or {}

    def get(self, *args, **kwargs):
        return self._data.get(*args, **kwargs)

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return repr(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __contains__(self, key):
        return key in self._data

    def __len__(self):
        return len(self._data)

    def __eq__(self, other):
        return self._data == other

    def items(self):
        return self._data.items()

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def get_data(self):
        return self._data
