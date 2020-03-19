import copy
from pathlib import Path
import munch
from ruamel.yaml import YAML


class DictContainer:
    """ Dictionary container """
    _yaml = YAML()

    def __init__(self, data=None):
        self.set_data_from_key(data or {})

    def get(self, *args, **kwargs):
        return self._sconf_data.get(*args, **kwargs)

    def __str__(self):
        return str(self._sconf_data.toDict())

    def __repr__(self):
        return repr(self._sconf_data.toDict())

    def __getitem__(self, key):
        return self._sconf_data[key]

    def __setitem__(self, key, value):
        self._sconf_data[key] = value

    def __getattr__(self, key):
        return self._sconf_data[key]

    def __setattr__(self, key, value):
        if key.startswith('_sconf_'):
            super().__setattr__(key, value)
        else:
            self._sconf_data[key] = value

    def __contains__(self, key):
        return key in self._sconf_data

    def __len__(self):
        return len(self._sconf_data)

    def __eq__(self, other):
        return self._sconf_data == other

    def items(self):
        return self._sconf_data.items()

    def keys(self):
        return self._sconf_data.keys()

    def values(self):
        return self._sconf_data.values()

    def get_data(self):
        return self._sconf_data

    def set_data_from_key(self, key):
        """ Set data from key

        Args:
            key (dict, str, pathlib.Path): data dictionary or data path
        """
        data = self._load_key(key)
        self._sconf_data = data

    def _load_key(self, key):
        """ Load data from key

        Args:
            key (dict, str, pathlib.Path): data dictionary or data path
        """
        if isinstance(key, dict):
            dic = copy.deepcopy(key)
        elif isinstance(key, (str, Path)):
            dic = self._yaml.load(open(key))
        else:
            raise ValueError(
                "Key should be dict, str, or pathlib.Path, but {} is given".format(type(key))
            )

        return munch.Munch.fromDict(dic)
