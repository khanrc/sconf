import pytest
from ruamel.yaml import YAML
from sconf import Config

yaml = YAML()


def test_basic():
    dic = yaml.load("""
        test: 1
        hmm: 2
        a:
            q: 1
            w: 2
    """)
    cfg = Config(dic)

    assert cfg['test'] == 1
    assert cfg['hmm'] == 2
    assert cfg['a']['q'] == 1
    assert cfg['a']['w'] == 2
    assert len(cfg) == 3
    assert len(cfg['a']) == 2


def test_modify():
    dic = yaml.load("""
        test: 1
        hmm: 2
        a:
            q: 1
            w: 2
    """)
    cfg = Config(dic)
    cfg['a']['r'] = 3
    cfg['a']['z'] = True
    cfg['a']['q'] = 2

    assert len(cfg['a']) == 4
    assert cfg['a']['z']
    assert cfg['a']['q'] == 2


def test_merge():
    dic1 = yaml.load("""
        test: 1
        hmm: 2
        a:
            q: 1
            w: 2
    """)
    dic2 = yaml.load("""
        test: 2
        hmm: 3
        a:
            w: 8
            c: 6
        b:
            bq: 1
            bw: 2
    """)
    cfg = Config(dic1, dic2)

    assert cfg['test'] == 2
    assert cfg['hmm'] == 3
    assert len(cfg['a']) == 3
    assert len(cfg['b']) == 2
    assert cfg['a']['w'] == 8
    assert cfg['a']['c'] == 6


def test_true():
    dic = yaml.load("""
        test: True
        hmm: true
        a:
            q: TRUE
            w: tRuE
    """)
    cfg = Config(dic)

    assert cfg['test'] == True
    assert cfg['hmm'] == True
    assert cfg['a']['q'] == True
    assert cfg['a']['w'] == 'tRuE'


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


def test_false():
    dic = yaml.load("""
        a: false
        b: FAlse
        c: faLSE
    """)
    cfg = Config(dic)

    assert cfg['a'] == False
    assert cfg['b'] == 'FAlse'
    assert cfg['c'] == 'faLSE'


def test_none():
    dic = yaml.load("""
        a: None
        b: none
        c: NONE
    """)
    cfg = Config(dic)

    assert cfg['a'] == 'None'
    assert cfg['b'] == 'none'
    assert cfg['c'] == 'NONE'


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


def test_null():
    dic = yaml.load("""
        d: Null
        e: null
        f: NULL
        g: NUll
    """)
    cfg = Config(dic)

    assert cfg['d'] is None
    assert cfg['e'] is None
    assert cfg['f'] is None
    assert cfg['g'] == 'NUll'


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
