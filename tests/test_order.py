import pytest
from ruamel.yaml import YAML
from sconf import Config

yaml = YAML()


def test_order():
    dic = yaml.load("""
        a: 1
        b: 2
        c:
            q: 1
            w: 2
    """)
    cfg = Config(dic)

    assert list(dic.keys()) == ['a', 'b', 'c']
    assert list(dic['c'].keys()) == ['q', 'w']


def test_modified_order():
    dic = yaml.load("""
        a: 1
        b: 2
        c:
            q: 1
            w: 2
    """)
    cfg = Config(dic)

    dic['b'] = 3

    assert list(dic.keys()) == ['a', 'b', 'c']


def test_newkey_order():
    dic = yaml.load("""
        a: 1
        b: 2
        c:
            q: 1
            w: 2
    """)
    cfg = Config(dic)

    dic['b'] = 3
    dic['d'] = 1
    dic['c']['a'] = 0

    assert list(dic.keys()) == ['a', 'b', 'c', 'd']
    assert list(dic['c'].keys()) == ['q', 'w', 'a']
