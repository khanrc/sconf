import sys
import io
import copy
from pathlib import Path

from ruamel.yaml import YAML

from .container import DictContainer
from .utils import colorize, type_infer, kv_iter, add_repr_to_yaml


class Config(DictContainer):
    _yaml = YAML()

    def __init__(self, *keys, default=None, colorize_modified_item=True):
        """
        Args:
            keys (str, dict): yaml path or loaded dict
            default (str, dict): default key
            colorize_modified_item (bool)
        """
        super().__init__()
        self.colorize_modified_item = colorize_modified_item

        if default:
            keys = (default,) + keys

        if keys:
            self.data = self._load(keys[0])
            keys = keys[1:]

        for key in keys:
            self._dict_update(self._load(key))

        self._build_keydic()
        self._modified = {}

    def _load(self, key):
        if isinstance(key, dict):
            return copy.deepcopy(key)
        elif isinstance(key, (str, Path)):
            return self._yaml.load(open(key))
        else:
            raise ValueError()

    def _dict_update(self, dic):
        """ update self.data from dic - support nested dic """
        def merge(base, supp):
            """ Merge supplementary dict into base dict """
            for k in supp.keys():
                if isinstance(supp[k], dict) and k in base:
                    assert isinstance(base[k], dict), "cannot update single value to dict"
                    merge(base[k], supp[k])
                else:
                    base[k] = supp[k]

        if dic is not None:
            merge(self.data, dic)

    def _build_keydic(self):
        """ Build key dictionary; keydic[flat_key] = lastdic """
        def build_keydic(data, prefix, keydic):
            for k, v in kv_iter(data):
                key = "{}.{}".format(prefix, k)
                keydic[key] = data
                if isinstance(v, (dict, list)):
                    build_keydic(v, key, keydic)

        self._keydic = {}
        build_keydic(self.data, '', self._keydic)

    def argv_update(self, argv=None):
        """ Update self.data using argv
        argv structure: [option1, value1, option2, value2, ...]
        If argv is not given, use sys.argv[1:] as default.
        """
        if argv is None:
            argv = sys.argv[1:]

        N = len(argv)
        if N % 2 != 0:
            raise ValueError("Key-value should be paired, but given argv = {}".format(argv))

        for i in range(0, N, 2):
            flat_key, value = argv[i:i+2]
            self._update(flat_key, value)

        self._build_keydic()

    def _update(self, flat_key, value):
        """ Update self.data using flat_key and value

        Args:
            flat_key: hierarchical (partial) flat key with:
                "--": must single-match
                "---": allow multi-match
                e.g.) "--model.n_layers" or "---self_attention"
            value
        """
        index = 0
        while flat_key[index] == '-':
            index += 1
        if index not in {2, 3}:
            raise ValueError("Key should have `--` or `---` prefix, but {}".format(flat_key))
        flat_key = flat_key[index:]

        lasts = self._find_lastdic(flat_key)
        key = flat_key.split('.')[-1]

        # single match case
        if index == 2 and len(lasts) != 1:
            raise ValueError("-- key should match to only single item, but {}".format(len(lasts)))

        for last in lasts:
            if isinstance(last, list):
                key = int(key)
                if key == len(last):
                    last.append(None)  # extend list
            last[key] = type_infer(value)

            if self.colorize_modified_item:
                self._modified.setdefault(id(last), set()).add(key)

    def _find_lastdic(self, flat_key):
        """ Find parent dictionary of given flat_key """
        def get_parentkey(key):
            return key[:key.rindex('.')]

        key = '.' + flat_key
        key_parent = get_parentkey(key)
        ret = []
        cand = {}
        for k, v in self._keydic.items():
            k_parent = get_parentkey(k)
            if k.endswith(key):
                ret.append(v)
            elif k_parent.endswith(key_parent):
                cand[k_parent] = v

        # add new argument
        if not ret and len(cand) == 1:
            return [cand.popitem()[1]]

        return ret

    def yamls(self):
        out = io.StringIO()
        Config._yaml.dump(self.data, out)
        return out.getvalue().strip()

    def dumps(self, modified_color=36, quote_str=False):
        """ Dump to colorized string
        Args:
            modified_color: color for modified item
            quote_str: quoting string for identifying string and keyword
        """
        strs = []
        tab = '  '

        def quote(v):
            if quote_str and isinstance(v, str) and v:
                return "'{}'".format(v)
            return v

        def repr_dict(k, v):
            if isinstance(v, (dict, list)):
                v = ''
            return "{}: {}\n".format(k, quote(v))

        def repr_list(_k, v):
            if isinstance(v, (dict, list)):
                return "- "
            return "- {}\n".format(quote(v))

        def dump(data, indent, firstline_nopref=False):
            modified = self._modified.get(id(data), set())

            for k, v in kv_iter(data):
                prefix = indent
                if firstline_nopref:
                    prefix = ''
                    firstline_nopref = False

                # representation is determined by parent data type
                if isinstance(data, dict):
                    s = repr_dict(k, v)
                    skip_first_indent = False
                elif isinstance(data, list):
                    s = repr_list(k, v)
                    skip_first_indent = True
                else:
                    raise ValueError(type(data))

                if k in modified:
                    s = colorize(s, modified_color)
                strs.append(prefix + s)
                if isinstance(v, (dict, list)):
                    dump(v, indent + tab, skip_first_indent)

        dump(self.data, '')
        strs[-1] = strs[-1].rstrip('\n')  # remove last newline
        return ''.join(strs)

    @staticmethod
    def add_yaml_repr(add_cls, tag, instance_repr_fn=str):
        """ Add yaml representation
        If you use custom class, including python builtin, you should specify
        the representation for the `yamls()` dumping function.

        Args:
            add_cls: adding class to yaml representation
            tag: representation tag
            instance_repr_fn: instance representor function
        """
        add_repr_to_yaml(Config._yaml, add_cls, tag, instance_repr_fn)
