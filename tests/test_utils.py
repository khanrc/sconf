import pytest
from sconf.utils import kv_iter


def test_kviter():
    # test dict
    dic = {'a': 1, 'b': 2}
    iterator = kv_iter(dic)
    assert ('a', 1) == next(iterator)
    assert ('b', 2) == next(iterator)

    # test list
    lst = ['a', 'b']
    iterator = kv_iter(lst)
    assert (0, 'a') == next(iterator)
    assert (1, 'b') == next(iterator)

    # test error (non-iterable)
    with pytest.raises(ValueError) as excinfo:
        kv_iter(1)

    assert isinstance(excinfo.value, ValueError)
