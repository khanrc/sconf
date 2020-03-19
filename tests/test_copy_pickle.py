import pytest
import copy
import pickle
import tempfile
from sconf import Config


def test_copy(train_cfg):
    # copy of sconf is same as deepcopy
    c = copy.copy(train_cfg)
    c.lr = 0.1
    c.model.encoder.n_channels = 32

    assert train_cfg.lr == 0.001
    assert train_cfg.model.encoder.n_channels == 64


def test_deepcopy(train_cfg):
    c = copy.deepcopy(train_cfg)
    c.lr = 0.1
    c.model.encoder.n_channels = 32

    assert train_cfg.lr == 0.001
    assert train_cfg.model.encoder.n_channels == 64


# TODO for now (0.2.0), deepcopying sconf cannot preserve modified items,
# since it identify each key by its reference.
#  def test_deepcopy_color(train_cfg):
#      # test out-of-data attributes
#      dic = {
#          'a': 10,
#          'b': 20
#      }
#      cfg = Config(dic, colorize_modified_item=True)
#      c_org = copy.deepcopy(cfg)

#      cfg.argv_update([
#          '--a', '20'
#      ])
#      c_modified = copy.deepcopy(cfg)

#      cfg.argv_update([
#          '--a', '30'
#      ])

#      assert c_org.dumps() == "a: 10\nb: 20"
#      assert c_modified.dumps() == "\033[36ma: 20\n\033[0mb: 20"
#      assert c_modified.dumps(modified_color=None) == "a: 20\nb: 20"


def test_pickle(train_cfg):
    with tempfile.TemporaryFile() as temp:
        train_cfg.lr = 0.1
        pickle.dump(train_cfg, temp)
        train_cfg.lr = 0.2
        train_cfg.betas[0] = 0.

        temp.seek(0)
        cfg = pickle.load(temp)
        assert cfg.lr == 0.1
        assert cfg.betas == [0.5, 0.9]
