import pytest
from ruamel.yaml import YAML
from sconf import Config, dump_args

yaml = YAML()


def test_dumps():
    dic = yaml.load("""
        test: 1
        hmm: 2
        a:
            q: 1
            w: 2
        b:
            - 1
            - 2
            - 3
        c:
            - a: 10
              b: 10
            - q: 20
              w: 20
    """)
    cfg = Config(dic, colorize_modified_item=False)

    dic2 = yaml.load(cfg.dumps())

    assert dic == dic2


def test_dumps_coloring():
    dic = yaml.load("""
        a: 10
        b: 20
    """)
    cfg = Config(dic, colorize_modified_item=True)
    cfg.argv_update([
        '--a', '20'
    ])

    assert cfg.dumps() == "\033[36ma: 20\n\033[0mb: 20"
    assert cfg.dumps() == "\x1b[36ma: 20\n\x1b[0mb: 20"  # hexa
    assert cfg.dumps(modified_color=None) == "a: 20\nb: 20"


def test_dumps_quote():
    dic = yaml.load("""
        a: null
        b: None
        c: 1
        d: 1.1
    """)
    cfg = Config(dic, colorize_modified_item=True)

    assert cfg.dumps(quote_str=True) == "a: None\nb: 'None'\nc: 1\nd: 1.1"


def test_dump_args():
    import argparse
    parser = argparse.ArgumentParser("TEST")
    parser.add_argument("a")
    parser.add_argument("b")
    parser.add_argument("--beta")
    parser.add_argument("B")
    parser.add_argument("AA")
    parser.add_argument("--alpha")

    args = parser.parse_args(args="1 2 3 4 --beta 5 --alpha 6".split())
    dumps = dump_args(args)

    assert dumps == "\n".join([
        "a     = 1",
        "b     = 2",
        "beta  = 5",
        "B     = 3",
        "AA    = 4",
        "alpha = 6"
    ])
