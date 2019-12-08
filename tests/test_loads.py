import pytest
from ruamel.yaml import YAML
from sconf import Config

yaml = YAML()


def test_load_from_filepath(tmp_path, train_dic, train_cfg, data_dic, data_cfg, merge_cfg):
    train_path = tmp_path / 'train.yaml'
    data_path = tmp_path / 'data.yaml'
    yaml.dump(train_dic, train_path)
    yaml.dump(data_dic, data_path)

    cfg = Config(train_path)
    assert train_cfg == cfg

    cfg = Config(data_path)
    assert data_cfg == cfg

    cfg = Config(train_path, data_path)
    assert merge_cfg == cfg

    cfg = Config(data_path, default=train_path)
    assert merge_cfg == cfg


def test_wrong_key():
    with pytest.raises(ValueError) as excinfo:
        cfg = Config(123)

    assert isinstance(excinfo.value, ValueError)


def test_empty():
    cfg = Config()
    assert len(cfg) == 0
    assert not cfg


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
