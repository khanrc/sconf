from sconf import dump_args


def test_dump_args():
    import argparse
    parser = argparse.ArgumentParser("TEST")
    parser.add_argument("a")
    parser.add_argument("b")
    parser.add_argument("--beta")
    parser.add_argument("B")
    parser.add_argument("AA")
    parser.add_argument("--alpha")

    args = parser.parse_args(args="1 2 3 4 --beta 5 --alpha 6".split())
    dumps = dump_args(args)

    assert dumps == "\n".join([
        "a     = 1",
        "b     = 2",
        "beta  = 5",
        "B     = 3",
        "AA    = 4",
        "alpha = 6"
    ])
