import argparse
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
    ])

    assert train_cfg['lr'] == 0.1
    assert train_cfg['batch_size'] == 64
    assert train_cfg['betas'][0] == 0.
    assert data_cfg['ignore_list'][0]['value'] == 1.2
    assert data_cfg['ignore_list'][1]['value'] == 1.3


def test_insert_container_into_value(train_cfg):
    lr = [1, 2, 3]
    batch_size = {'a': 1, 'b': 2, 'c': 3}
    train_cfg.argv_update([
        '--lr', str(lr),
        '--batch_size', str(batch_size)
    ])

    assert train_cfg.lr == lr
    assert train_cfg.batch_size == batch_size


def test_default_argv(train_cfg):
    argv = [
        'train.py',
        '---n_channels', '32'
    ]
    with mock.patch('sys.argv', argv):
        train_cfg.argv_update()

    assert train_cfg['model'] == {
        'encoder': {
            'n_channels': 32,
        },
        'decoder': {
            'n_channels': 32,
        }
    }


def test_with_argparse_noleft(train_cfg, train_dic):
    parser = argparse.ArgumentParser('Test')
    parser.add_argument('name')
    parser.add_argument('config_paths', nargs='+')
    parser.add_argument('--show', default=False, action='store_true')

    argv = ['train.py', 'test', 'configs/test.yaml', '--show']
    with mock.patch('sys.argv', argv):
        args, left_argv = parser.parse_known_args()
        train_cfg.argv_update(left_argv)

    assert dict(train_cfg) == dict(train_dic)


def test_with_argparse(train_cfg, train_dic):
    parser = argparse.ArgumentParser('Test')
    parser.add_argument('name')
    parser.add_argument('config_paths', nargs='+')
    parser.add_argument('--show', default=False, action='store_true')

    argv = ['train.py', 'test', 'configs/test.yaml', '--lr', '0.1', '--batch_size', '64']
    with mock.patch('sys.argv', argv):
        args, left_argv = parser.parse_known_args()
        train_cfg.argv_update(left_argv)

    train_dic['lr'] = 0.1
    train_dic['batch_size'] = 64
    assert dict(train_cfg) == dict(train_dic)
