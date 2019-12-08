import pytest
from unittest import mock


def test_cli(train_cfg, data_cfg):
    train_cfg.argv_update([
        '--lr', '0.1',
        '--batch_size', '64',
        '--betas.0', '0.'
    ])
    data_cfg.argv_update([
        '--ignore_list.0.value', '1.2',
        '--1.value', '1.3',
        '--ignore_list.2', 3
    ])

    assert train_cfg['lr'] == 0.1
    assert train_cfg['batch_size'] == 64
    assert train_cfg['betas'][0] == 0.
    assert data_cfg['ignore_list'][0]['value'] == 1.2
    assert data_cfg['ignore_list'][1]['value'] == 1.3
    assert data_cfg['ignore_list'][2] == 3


def test_default_argv(train_cfg):
    argv = [
        'train.py',
        '--encoder.norm', 'BN',
        '--decoder.norm', 'IN',
        '---n_channels', '32'
    ]
    with mock.patch('sys.argv', argv):
        train_cfg.argv_update()

    assert train_cfg['model'] == {
        'encoder': {
            'n_channels': 32,
            'norm': 'BN'
        },
        'decoder': {
            'n_channels': 32,
            'norm': 'IN'
        }
    }
