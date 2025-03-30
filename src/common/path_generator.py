

from collections.abc import Iterator


def tokenizer(number: int):
    """
    Convert a number to a unique string consisting of the letters a and b
    :param number:
    :return:
    """

    converted_to_bin = bin(number).split("b")[1]

    converted_to_bin = converted_to_bin.replace("0", "a")
    return converted_to_bin.replace("1", "b")


def path_generator(
        n: int,
        n_shift: int = 0,
        str_postfix: str = "",
        int_postfix: str = ""
) -> Iterator[str]:

    for i in range(n):
        first = "{first" + str_postfix + "}"
        second = "{second" + int_postfix + "}"

        yield f'/{tokenizer(i+n_shift)}/1234/{tokenizer(i+n_shift)}/{first}/{second}'
