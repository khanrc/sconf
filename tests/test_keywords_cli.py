import pytest
from ruamel.yaml import YAML
from sconf import Config

yaml = YAML()


def test_true_cli():
    dic = yaml.load("""
        test: True
        hmm: true
        a:
            q: TRUE
            w: tRuE
    """)
    cfg = Config(dic)
    cfg.argv_update(['--test', 'true', '--hmm', 'True', '--a.q', 'trUE', '--a.w', 'TRUE'])

    assert cfg['test'] == True
    assert cfg['hmm'] == True
    assert cfg['a']['q'] == 'trUE'
    assert cfg['a']['w'] == True


def test_false_cli():
    dic = yaml.load("""
        a: false
        b: FAlse
        c: faLSE
    """)
    cfg = Config(dic)
    cfg.argv_update(['--a', 'False', '--b', 'false', '--c', 'FALSE', '--d', 'Fals', '--e', 'FAlse'])

    assert cfg['a'] == False
    assert cfg['b'] == False
    assert cfg['c'] == False
    assert cfg['d'] == 'Fals'
    assert cfg['e'] == 'FAlse'


def test_none_cli():
    dic = yaml.load("""
        a: 1
        b: 2
        c: 3
    """)
    cfg = Config(dic)
    cfg.argv_update(['--a', 'None', '--b', 'NONE', '--c', 'none', '--d', 'NOne'])

    assert cfg['a'] == 'None'
    assert cfg['b'] == 'NONE'
    assert cfg['c'] == 'none'
    assert cfg['d'] == 'NOne'


def test_null_cli():
    dic = yaml.load("""
        a: 1
        b: 2
        c: 3
    """)
    cfg = Config(dic)
    cfg.argv_update(['--a', 'null', '--b', 'Null', '--c', 'NULL', '--d', 'NUll', '--e', '\'Null\''])

    assert cfg['a'] is None
    assert cfg['b'] is None
    assert cfg['c'] is None
    assert cfg['d'] == 'NUll'
    assert cfg['e'] == 'Null'
