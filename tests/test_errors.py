import pytest


def test_missing_key(train_cfg):
    with pytest.raises(ValueError):
        train_cfg.argv_update(['--lr', '0.1', '--batch_size'])


def test_missing_value(train_cfg):
    with pytest.raises(ValueError):
        train_cfg.argv_update(['--lr', '0.1', '128'])


@pytest.mark.parametrize("argv", [
    ('lr', '0.1'),
    ('-lr', '0.1'),
    ('**lr', '0.1'),
    ('++lr', '0.1'),
    ('----lr', '0.1'),
])
def test_wrong_prefix(train_cfg, argv):
    with pytest.raises(ValueError):
        train_cfg.argv_update(argv)


def test_wrong_multi_match(train_cfg):
    with pytest.raises(ValueError):
        train_cfg.argv_update(['--n_channels', '32'])


def test_not_matched(train_cfg):
    with pytest.raises(ValueError):
        train_cfg.argv_update(['--model.disc.n_channels', '32'])


def test_error_on_newkey(train_cfg):
    with pytest.raises(ValueError):
        train_cfg.argv_update([
            '--newkey', '1'
        ])

    with pytest.raises(ValueError):
        train_cfg.argv_update([
            '--model.newkey', '1'
        ])

    with pytest.raises(ValueError):
        train_cfg.argv_update([
            '--model.encoder.newkey', '1'
        ])
