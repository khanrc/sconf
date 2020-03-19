import pytest
from sconf import Config


def test_basic(train_cfg, train_dic):
    assert train_cfg.lr == train_dic['lr']
    assert train_cfg.model.encoder.n_channels == train_dic['model']['encoder']['n_channels']
    assert train_cfg.betas[0] == train_dic['betas'][0]
    assert train_cfg.betas[1] == train_dic['betas'][1]


def test_complicate(data_cfg, data_dic):
    assert data_cfg.ignore_list[0].name == data_dic['ignore_list'][0]['name']
    assert data_cfg.ignore_list[1].value == data_dic['ignore_list'][1]['value']


def test_modify(train_cfg):
    train_cfg.batch_size = 64
    train_cfg.betas[0] = 0.
    train_cfg.model.encoder.n_layers = 4

    assert train_cfg.batch_size == train_cfg['batch_size'] == 64
    assert train_cfg.betas == train_cfg['betas'] == [0.0, 0.9]
    assert train_cfg.model.encoder.n_layers == train_cfg['model']['encoder']['n_layers'] == 4


def test_duplicated_key_for_container():
    """ Duplicated key test for config container """
    # With the dot-access interface, we cannot use the duplicated keys with object method name.
    duplicated_dic = {
        "get": 1,
        "items": 2,
    }
    cfg = Config(duplicated_dic)

    assert cfg['get'] == 1
    assert cfg['items'] == 2

    # dot access to the duplicated key should return the method but value.
    assert cfg.get != 1 and callable(cfg.get)
    assert cfg.items != 2 and callable(cfg.items)


def test_duplicated_key_for_dotdict():
    """ Duplicated key test for inner data structure (e.g. Munch) """
    duplicated_dic = {
        't': {
            "get": 1,
            "items": 2,
            "update": 3,
        }
    }
    cfg = Config(duplicated_dic)

    assert cfg['t']['get'] == 1
    assert cfg['t']['items'] == 2
    assert cfg['t']['update'] == 3

    # dot access to the duplicated key should return the method but value.
    assert cfg.t.get != 1 and callable(cfg.t.get)
    assert cfg.t.items != 2 and callable(cfg.t.items)
    assert cfg.t.update != 3 and callable(cfg.t.update)
