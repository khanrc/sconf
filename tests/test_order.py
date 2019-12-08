import pytest
from sconf import Config


def test_order(train_cfg):
    assert list(train_cfg.keys()) == ['lr', 'batch_size', 'model', 'optim', 'betas']
    assert list(train_cfg['model'].keys()) == ['encoder', 'decoder']


def test_modified_order(train_cfg):
    train_cfg['batch_size'] = 64
    train_cfg['lr'] = 0.1
    assert list(train_cfg.keys()) == ['lr', 'batch_size', 'model', 'optim', 'betas']


def test_newkey_order(train_cfg):
    train_cfg['steps'] = 10000
    train_cfg['model']['encoder']['kernel_size'] = 5

    assert list(train_cfg.keys()) == ['lr', 'batch_size', 'model', 'optim', 'betas', 'steps']
    assert list(train_cfg['model']['encoder'].keys()) == ['n_channels', 'kernel_size']


def test_merge_order(train_dic, data_dic):
    cfg = Config(train_dic, data_dic)
    cfg_reverse = Config(data_dic, train_dic)

    # same content
    assert dict(cfg) == dict(cfg_reverse)

    # different order
    assert list(cfg.keys()) != list(cfg_reverse.keys())
