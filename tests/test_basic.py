import pytest
from ruamel.yaml import YAML
from sconf import Config

yaml = YAML()


def test_eq():
    dic = yaml.load("""
        test: 1
        hmm: 2
        a:
            q: 1
            w: 2
    """)
    cfg = Config(dic)

    assert cfg == {
        'test': 1,
        'hmm': 2,
        'a': {
            'q': 1,
            'w': 2
        }
    }
    assert cfg != {
        'test': 1,
        'hmm': 2,
        'a': {
            'q': 2,
            'w': 2
        }
    }


def test_len():
    dic = yaml.load("""
        test: 1
        hmm: 2
        a:
            q: 1
            w: 2
    """)
    cfg = Config(dic)

    assert len(cfg) == 3
    assert len(cfg['a']) == 2


def test_contain():
    dic = yaml.load("""
        test: 1
        hmm: 2
        a:
            q: 1
            w: 2
    """)
    cfg = Config(dic)

    assert 'test' in cfg
    assert 'hmm' in cfg
    assert 'a' in cfg
    assert 'q' in cfg['a']
    assert 'w' in cfg['a']


def test_get():
    dic = yaml.load("""
        test: 1
        hmm: 2
        a:
            q: 1
            w: 2
    """)
    cfg = Config(dic)

    assert cfg.get('test') == 1
    assert cfg.get('non-key') is None
    assert cfg.get('b', 'default') == 'default'
    assert cfg.get('a').get('q') == 1


def test_str_repr():
    dic = yaml.load("""
        test: 1
        hmm: 2
        a:
            q: 1
            w: 2
    """)
    cfg = Config(dic)

    assert repr(cfg) == repr(cfg.data)
    assert str(cfg) == str(cfg.data)


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
