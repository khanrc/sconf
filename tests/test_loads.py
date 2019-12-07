import pytest
from ruamel.yaml import YAML
from sconf import Config

yaml = YAML()


def test_load_from_dict():
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
    assert len(cfg) == 3


def test_load_from_filepath(tmp_path):
    data = {
        'test': 1,
        'hmm': 2,
        'a': {
            'q': 1,
            'w': 2
        }
    }
    path = tmp_path / 'test.yaml'
    yaml.dump(data, path)

    cfg = Config(path)

    assert cfg == data


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

    assert cfg == {
        'b': [1,2,3],
        'c': [
            {'a': 10, 'b': 10},
            {'q': 20, 'w': 20}
        ]
    }


def test_empty():
    cfg = Config()
    assert len(cfg) == 0
    assert not cfg


def test_default():
    dic = yaml.load("""
        test: 1
        hmm: 2
        a:
            q: 1
            w: 2
    """)
    cfg = Config(default=dic)

    assert cfg == {
        'test': 1,
        'hmm': 2,
        'a': {
            'q': 1,
            'w': 2
        }
    }


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

    assert cfg == {
        'test': 2,
        'hmm': 3,
        'a': {
            'q': 1,
            'w': 8,
            'c': 6
        },
        'b': {
            'bq': 1,
            'bw': 2
        }
    }
