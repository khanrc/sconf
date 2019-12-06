import pytest
from ruamel.yaml import YAML
from sconf import Config

yaml = YAML()


def test_load():
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


def test_wrong_key():
    with pytest.raises(ValueError) as excinfo:
        cfg = Config(123)

    assert isinstance(excinfo.value, ValueError)


def test_list():
    dic = yaml.load("""
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
    cfg = Config(dic)

    assert len(cfg) == 2
    assert len(cfg['b']) == 3
    assert len(cfg['c']) == 2
    assert cfg['b'] == [1, 2, 3]
    assert cfg['c'][0]['a'] == 10
    assert cfg['c'][0]['b'] == 10
    assert cfg['c'][1]['q'] == 20
    assert cfg['c'][1]['w'] == 20



def test_empty():
    cfg = Config()
    assert len(cfg) == 0


def test_default():
    dic = yaml.load("""
        test: 1
        hmm: 2
        a:
            q: 1
            w: 2
    """)
    cfg = Config(default=dic)

    assert cfg['test'] == 1
    assert cfg['hmm'] == 2
    assert cfg['a']['q'] == 1
    assert cfg['a']['w'] == 2
    assert len(cfg) == 3
    assert len(cfg['a']) == 2


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
