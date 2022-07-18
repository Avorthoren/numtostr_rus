from typing import Union

from .db import BASIC_WORDS


BASE = 10
BASE2 = BASE * BASE


# TODO: implement float, Decimal, Rational, Complex.
#       After implementing Complex, next line should be
#       Num_T = numbers.Complex
Num_T = Union[int]

# TODO: implement ONES_MODE:
#       REGULAR: один триллион одна тысяча
#       SHORT: миллиард тысяча
#       LONG: один миллиард ноль миллионов одна тысяча

# TODO: implement add_plus flag for adding explicit word for '+' sign.

# TODO: implement SCALE:
#       SHORT: триллион == 10**12
#       LONG: триллион == 10**18

# TODO: implement capitalize flag for capitalizing first word.


def convert(num: Num_T) -> str:
	"""Main function of the package."""
	if num == 0:
		return BASIC_WORDS[0]

	if num < 0:
		minus = True
		num = -num
	else:
		minus = False

	num_str = _convert(num)

	return f"{'минус ' if minus else ''}{num_str}"


def _convert(num: int) -> str:
	return _before1000(num)


def _before20(num: int) -> str:
	assert 0 <= num < 20
	if num == 0:
		return ''
	return BASIC_WORDS[num]


def _before100(num: int) -> str:
	assert 0 <= num < 100
	if num < 20:
		return _before20(num)

	r = num % BASE
	return f"{BASIC_WORDS[num - r]} {_before20(r)}"


def _before1000(num: int) -> str:
	assert 0 <= num < 1000
	if num < 100:
		return _before100(num)

	r = num % BASE2
	return f"{BASIC_WORDS[num - r]} {_before100(r)}"
