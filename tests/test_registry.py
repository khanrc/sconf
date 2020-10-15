import pytest
from sconf import Config, registry


# NOTE the registry is maintained globally. So, reset first to remove different-file dependency.
def test_reset():
    registry.reset()

    with pytest.raises(KeyError):
        registry.get('default')


# train_cfg is default config in registry.
def test_reg(train_cfg):
    cfg = Config.from_registry()

    assert train_cfg == cfg


def test_reg2(train_cfg, data_cfg):
    cfg = Config.from_registry()

    assert train_cfg == cfg
    assert data_cfg != cfg


def test_new_registration(train_cfg, data_cfg):
    registry.register(data_cfg, 'data')
    cfg = Config.from_registry('data')

    assert train_cfg != cfg
    assert data_cfg == cfg


def test_duplicated_key(train_cfg):
    # the key 'data' is registered already in the last function.
    with pytest.raises(ValueError):
        registry.register(train_cfg, 'data')

    with pytest.raises(ValueError):
        registry.register(train_cfg, 'default')

    registry.register(train_cfg, 'default', ignore_duplicated_error=True)


def test_modify_data():
    cfg = Config.from_registry()
    assert cfg.lr == 0.001
    cfg.lr = 0.1


def test_is_maintained():
    cfg = Config.from_registry()
    assert cfg.lr == 0.1


def test_is_diff_to_given(train_cfg):
    cfg = Config.from_registry()
    assert train_cfg != cfg
    cfg.lr = 0.001
    assert train_cfg == cfg
    assert id(train_cfg) != id(cfg)
