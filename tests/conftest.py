""" shared fixtures through session """
import io
import pytest
from ruamel.yaml import YAML
from sconf import Config

yaml = YAML()


def dump_to_string(data):
    stream = io.StringIO()
    yaml.dump(data, stream)
    return stream.getvalue()


@pytest.fixture
def load_cfg():
    return Config("tests/assets/default.yaml")


@pytest.fixture
def train_dic():
    dic = {
        'lr': 0.001,
        'batch_size': 128,
        'model': {
            'encoder': {
                'n_channels': 64
            },
            'decoder': {
                'n_channels': 64
            }
        },
        'optim': 'adam',
        'betas': [0.5, 0.9],
    }
    return dic


@pytest.fixture
def data_dic():
    dic = {
        'data_dir': '/data/dir/sconf/',
        'min_freq': 4,
        'ignore': True,
        'ignore_list': [
            {
                'name': 'first',
                'value': 1.1
            },
            {
                'name': 'second',
                'value': 1.2
            }
        ]
    }
    return dic


@pytest.fixture
def train_str(train_dic):
    return dump_to_string(train_dic)


@pytest.fixture
def train_cfg(train_dic):
    return Config(train_dic)


@pytest.fixture
def data_str(data_dic):
    return dump_to_string(data_dic)


@pytest.fixture
def data_cfg(data_dic):
    return Config(data_dic)


@pytest.fixture
def merge_cfg(train_dic, data_dic):
    return Config(train_dic, data_dic)
