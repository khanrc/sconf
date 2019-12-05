import pytest
from ruamel.yaml import YAML
from sconf import Config

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

    print(dic)
    print(dic2)

    assert dic == dic2


def test_yaml():
    dic = yaml.load("""
        # comment
        test: a/b/c
        hmm: c/d/e
    """)
    cfg = Config(dic, colorize_modified_item=False)

    assert cfg.yaml() == "# comment\ntest: a/b/c\nhmm: c/d/e"


def test_representor():
    dic = yaml.load("""
        # comment
        test: a/b/c
        hmm: c/d/e
    """)
    cfg = Config(dic, colorize_modified_item=False)

    from pathlib import Path
    Config.add_yaml_repr(Path, 'path')
    cfg['test'] = Path(cfg['test'])
    cfg['hmm'] = Path(cfg['hmm'])

    assert cfg.yaml() == "# comment\ntest: !<path> a/b/c\nhmm: !<path> c/d/e"
