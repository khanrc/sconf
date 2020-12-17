from ruamel.yaml import YAML
from sconf import Config

yaml = YAML()


def test_true():
    dic = yaml.load("""
        test: True
        hmm: true
        a:
            q: TRUE
            w: tRuE
    """)
    cfg = Config(dic)

    assert cfg['test'] is True
    assert cfg['hmm'] is True
    assert cfg['a']['q'] is True
    assert cfg['a']['w'] == 'tRuE'


def test_false():
    dic = yaml.load("""
        a: false
        b: FAlse
        c: faLSE
    """)
    cfg = Config(dic)

    assert cfg['a'] is False
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
