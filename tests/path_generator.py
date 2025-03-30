

from src.common.path_generator import path_generator


def test_generator_len():
    n = 4
    generator = path_generator(n=4)

    assert len([*generator]) == n


def test_generator_values_small():
    generator = path_generator(n=2)

    assert [*generator] == [
        "/a/1234/a/{first}/{second}",
        "/b/1234/b/{first}/{second}"
    ]


def test_generator_values_for_shift():
    generator = path_generator(n=4)

    assert [*generator] == [
        "/a/1234/a/{first}/{second}",
        "/b/1234/b/{first}/{second}",
        "/ba/1234/ba/{first}/{second}",
        "/bb/1234/bb/{first}/{second}",
    ]


def test_generator_values_for_shift_and_prefixes():
    generator = path_generator(n=4, str_postfix=":str", int_postfix=":int")

    assert [*generator] == [
        "/a/1234/a/{first:str}/{second:int}",
        "/b/1234/b/{first:str}/{second:int}",
        "/ba/1234/ba/{first:str}/{second:int}",
        "/bb/1234/bb/{first:str}/{second:int}",
    ]


def test_generator_values_for_shift_and_n_shift():
    generator = path_generator(n=2, n_shift=2, str_postfix=":str", int_postfix=":int")

    assert [*generator] == [
        "/ba/1234/ba/{first:str}/{second:int}",
        "/bb/1234/bb/{first:str}/{second:int}",
    ]
