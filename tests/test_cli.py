import pytest
from unittest import mock
from ruamel.yaml import YAML
from sconf import Config

yaml = YAML()


def test_list():
    dic = yaml.load("""
        list:
            - 1
            - 2
            - dic: 10
              con: hi
    """)
    cfg = Config(dic)
    cfg.argv_update([
        '--list.0', '10',
        '--list.2.dic', '20',
        '--2.con', '30'
    ])

    assert cfg['list'][0] == 10
    assert cfg['list'][1] == 2
    assert cfg['list'][2]['dic'] == 20
    assert cfg['list'][2]['con'] == 30


def test_dic():
    dic = yaml.load("""
        batch_size: 128
        optim: adam
        model:
            encoder:
                C: 64
                norm: IN
            decoder:
                C: 64
                norm: BN
    """)
    cfg = Config(dic)
    cfg.argv_update([
        '--encoder.norm', 'BN',
        '--decoder.norm', 'IN',
        '---C', '32'
    ])

    assert cfg['model']['encoder']['C'] == 32
    assert cfg['model']['decoder']['C'] == 32
    assert cfg['model']['encoder']['norm'] == 'BN'
    assert cfg['model']['decoder']['norm'] == 'IN'


def test_default_argv():
    dic = yaml.load("""
        batch_size: 128
        optim: adam
        model:
            encoder:
                C: 64
                norm: IN
            decoder:
                C: 64
                norm: BN
    """)
    cfg = Config(dic)
    argv = [
        'train.py',
        '--encoder.norm', 'BN',
        '--decoder.norm', 'IN',
        '---C', '32'
    ]
    with mock.patch('sys.argv', argv):
        cfg.argv_update()

    assert cfg['model']['encoder']['C'] == 32
    assert cfg['model']['decoder']['C'] == 32
    assert cfg['model']['encoder']['norm'] == 'BN'
    assert cfg['model']['decoder']['norm'] == 'IN'
