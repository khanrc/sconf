import ast


def colorize(s, color):
    return "\033[{}m{}\033[0m".format(color, s)


def dump_args(args):
    """ Convert args (namedtuple) to printable string """
    s = ""
    key_len = max(map(len, vars(args).keys()))
    for attr, value in vars(args).items():
        line = "{:{key_len}s} = {}".format(attr, value, key_len=key_len)
        s += line + "\n"

    return s.rstrip("\n")


def type_infer(s):
    """ String to variable with type inference

    NOTE that yaml 1.2 has true, false, and null keywords,
    with all upper case, all lower case, or capital; e.g.) True, TRUE, true.

    NOTE that CLI modification work a little different, which use this `type_infer` function.
    In CLI modification, support true, false, and null keywords same as yaml,
    with case insensitive. Further, you can use None also (case sensitive).
    e.g.) --key1.key2 true => True
          --key1.key2 None => None
          --key1.key2 none => 'none'
    If you want to get the string of the keywords, like 'True' or 'None', use escaping:
    e.g.) --key1.key2 \'true\' => 'true'
          --key1.key2 "'true'" => 'true'
    """
    # XXX disable supporting None for consistency?
    try:
        ts = s.strip().lower()
        if ts == 'true':
            s = 'True'
        elif ts == 'false':
            s = 'False'
        elif ts == 'null':
            s = 'None'

        s = ast.literal_eval(s)
        return s
    except Exception:
        return s


def add_repr_to_yaml(yaml, cls, tag, instance_repr_fn=str):
    def custom_repr(representer, instance):
        return representer.represent_scalar(tag, instance_repr_fn(instance))

    yaml.representer.add_multi_representer(cls, custom_repr)


def kv_iter(ds):
    """ Iterator for key-value structure, list and dict """
    if isinstance(ds, list):
        return enumerate(ds)
    elif isinstance(ds, dict):
        return ds.items()
    else:
        raise ValueError(type(ds))
