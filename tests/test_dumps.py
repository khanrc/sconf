import pytest
from ruamel.yaml import YAML
from sconf import Config

yaml = YAML()


def test_dumps():
    dic = yaml.load("""
        test: 1
        hmm: 2
        a:
            q: 1
            w: 2
        b:
            - 1
            - 2
            - 3
        c:
            - a: 10
              b: 10
            - q: 20
              w: 20
    """)
    cfg = Config(dic, colorize_modified_item=False)

    dic2 = yaml.load(cfg.dumps())

    assert dic == dic2


def test_dumps_coloring():
    dic = yaml.load("""
        a: 10
        b: 20
    """)
    cfg = Config(dic, colorize_modified_item=True)
    cfg.argv_update([
        '--a', '20'
    ])

    assert cfg.dumps() == "\033[36ma: 20\n\033[0mb: 20"
    assert cfg.dumps() == "\x1b[36ma: 20\n\x1b[0mb: 20"  # hexa
    assert cfg.dumps(modified_color=None) == "a: 20\nb: 20"


def test_dumps_quote():
    dic = yaml.load("""
        a: null
        b: None
        c: 1
        d: 1.1
    """)
    cfg = Config(dic, colorize_modified_item=True)

    assert cfg.dumps(quote_str=True) == "a: None\nb: 'None'\nc: 1\nd: 1.1"


def test_yaml():
    dic = yaml.load("""
        # comment
        test: a/b/c
        hmm: c/d/e
    """)
    cfg = Config(dic, colorize_modified_item=False)

    assert cfg.yamls() == "# comment\ntest: a/b/c\nhmm: c/d/e"


def test_representor():
    dic = yaml.load("""
        # comment
        test: a/b/c
        hmm: c/d/e
    """)
    cfg = Config(dic, colorize_modified_item=False)

    from pathlib import Path
    cfg['test'] = Path(cfg['test'])
    cfg['hmm'] = Path(cfg['hmm'])

    Config.add_yaml_repr(Path, 'path')
    assert cfg.yamls() == "# comment\ntest: !<path> a/b/c\nhmm: !<path> c/d/e"


# NOTE ruamel.yaml works like Singleton, so even new Config object already has Path representor.
#  def test_representor_error():
#      dic = yaml.load("""
#          # comment
#          test: a/b/c
#          hmm: c/d/e
#      """)
#      cfg = Config(dic, colorize_modified_item=False)

#      from pathlib import Path
#      cfg['test'] = Path(cfg['test'])
#      cfg['hmm'] = Path(cfg['hmm'])

#      print(cfg.yamls())

#      with pytest.raises(Exception) as excinfo:
#          yamls = cfg.yamls()

#      assert str(excinfo.value) == 'cannot represent an object: a/b/c'
