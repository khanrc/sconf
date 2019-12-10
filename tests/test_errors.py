import argparse
import pytest


def test_missing_key(train_cfg):
    with pytest.raises(ValueError) as error:
        train_cfg.argv_update(['--lr', '0.1', '--batch_size'])

    assert str(error.value).startswith('Key-value should be paired')


def test_missing_value(train_cfg):
    with pytest.raises(ValueError) as error:
        train_cfg.argv_update(['--lr', '0.1', '128'])

    assert str(error.value).startswith('Key-value should be paired')


@pytest.mark.parametrize("argv", [
    ('lr', '0.1'),
    ('-lr', '0.1'),
    ('**lr', '0.1'),
    ('++lr', '0.1'),
    ('----lr', '0.1'),
])
def test_wrong_prefix(train_cfg, argv):
    with pytest.raises(ValueError) as error:
        train_cfg.argv_update(argv)

    assert str(error.value).startswith('Key should have `--` or `---` prefix')


def test_wrong_multi_match(train_cfg):
    with pytest.raises(ValueError) as error:
        train_cfg.argv_update(['--n_channels', '32'])

    assert str(error.value).startswith('-- key should match to only single item')


def test_not_matched(train_cfg):
    with pytest.raises(ValueError) as error:
        train_cfg.argv_update(['--model.disc.n_channels', '32'])

    assert str(error.value).startswith('-- key should match to only single item')
