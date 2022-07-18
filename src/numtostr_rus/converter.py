from itertools import chain
from typing import Union, Iterable

from .db import BASIC_WORDS


BASE = 10
BASE2 = BASE * BASE


# TODO: implement float, Decimal, Rational, Complex.
#       After implementing Complex, next line should be
#       Num_T = numbers.Complex
Num_T = Union[int]
Words_T = Iterable[str]

# TODO: implement ONES_MODE:
#       REGULAR: один миллиард одна тысяча
#       SHORT: миллиард тысяча
#       LONG: один миллиард ноль миллионов одна тысяча

# TODO: implement add_plus flag for adding explicit word for '+' sign.

# TODO: implement explicit_decimal flag for adding ' целых ноль десятых' to
#       float and Decimal numbers that have zero fractional part.

# TODO: implement SCALE:
#       SHORT: триллион == 10**12
#       LONG: триллион == 10**18

# TODO: implement capitalize flag for capitalizing first word.


def convert(num: Num_T) -> str:
	"""Main function of the package.
	Converts `num` to russian words representation.
	Only for int -1000 < num < 1000.
	"""
	if num == 0:
		return BASIC_WORDS[0]

	if num < 0:
		minus = True
		num = -num
	else:
		minus = False

	return _join(
		_sign(minus),
		_int_part(num)
	)


def _join(*args: Words_T) -> str:
	return ' '.join(
		arg
		for arg in chain(*args)
		if arg != ''
	)


def _sign(minus: bool) -> Words_T:
	if minus:
		yield 'минус'


def _int_part(num: int) -> Words_T:
	yield from _before1000(num)


def _before20(num: int) -> Words_T:
	assert 0 <= num < 20
	if num == 0:
		return

	yield BASIC_WORDS[num]


def _before100(num: int) -> Words_T:
	assert 0 <= num < 100
	if num < 20:
		yield from _before20(num)
		return

	r = num % BASE
	yield BASIC_WORDS[num - r]
	yield from _before20(r)


def _before1000(num: int) -> Words_T:
	assert 0 <= num < 1000
	if num < 100:
		yield from _before100(num)
		return

	r = num % BASE2
	yield BASIC_WORDS[num - r]
	yield from _before100(r)
