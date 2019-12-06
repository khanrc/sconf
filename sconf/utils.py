import ast


def colorize(s, color):
    if color is None:
        return s

    return "\033[{}m{}\033[0m".format(color, s)


def dump_args(args):
    """ Convert args (argparse.Namespace) to printable string """
    lines = []
    key_len = max(map(len, vars(args).keys()))
    for attr, value in vars(args).items():
        line = "{:{key_len}s} = {}".format(attr, value, key_len=key_len)
        lines.append(line)

    return "\n".join(lines)


def type_infer(s):
    """ String to variable with type inference

    NOTE that yaml 1.2 has true, false, and null keywords,
    with all upper case, all lower case, or capital; e.g.) True, TRUE, true.

    If you want to get the string of the keywords, like 'True' or 'None', use escaping:
    e.g.) --key1.key2 \'true\' => 'true'
          --key1.key2 "'true'" => 'true'
    """
    def capitalize_ul(s):
        """ Capitalize string only if s is upper or lower case """
        if s.isupper() or s.islower():
            return s.capitalize()
        return s

    try:
        # Special case
        # 1. Treat 'None' as 'None' string, not None keyword
        if s.strip() == 'None':
            s = '\'None\''

        ts = capitalize_ul(s)
        if ts == 'True':
            s = 'True'
        elif ts == 'False':
            s = 'False'
        elif ts == 'Null':
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
