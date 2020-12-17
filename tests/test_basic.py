def test_eq(train_cfg, train_dic):
    assert train_cfg == train_dic

    train_dic['lr'] = 0.1
    assert train_cfg != train_dic


def test_asdict(train_cfg, train_dic):
    assert train_cfg.asdict() == train_dic
    assert isinstance(train_cfg.asdict(), dict)
    assert isinstance(train_cfg.asdict()["model"], dict)
    assert isinstance(train_cfg.asdict()["model"]["encoder"], dict)


def test_len(train_cfg):
    assert len(train_cfg) == 5
    assert len(train_cfg['betas']) == 2


def test_contain(train_cfg):
    assert 'lr' in train_cfg
    assert 'batch_size' in train_cfg
    assert 'model' in train_cfg


def test_get(train_cfg):
    assert train_cfg.get('lr') == 0.001
    assert train_cfg.get('non-key') is None
    assert train_cfg.get('non-key', 'default') == 'default'


def test_pop(train_cfg):
    assert 'lr' in train_cfg
    assert train_cfg.pop('lr') == 0.001
    assert 'lr' not in train_cfg
    assert train_cfg.pop('lr', 3e-4) == 3e-4


def test_str_repr(train_cfg, train_dic):
    assert repr(train_cfg) == repr(train_dic)
    assert str(train_cfg) == str(train_dic)


def test_key_value_items(train_cfg, train_dic):
    assert train_cfg.items() == train_dic.items()
    assert train_cfg.keys() == train_dic.keys()
    assert list(train_cfg.values()) == list(train_dic.values())


def test_modify(train_cfg):
    train_cfg['lr'] = 0.1
    train_cfg['batch_size'] = 64
    train_cfg['steps'] = 10000

    assert train_cfg['lr'] == 0.1
    assert train_cfg['batch_size'] == 64
    assert train_cfg['steps'] == 10000
