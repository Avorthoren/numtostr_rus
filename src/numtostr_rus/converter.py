from itertools import chain
from typing import Union, Iterable, Tuple

from .db import BASE, BASE2, SIGNS, BASIC_WORDS, MULTS_DATA


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

# TODO: implement max_step to specify max multiplier (like 'миллиард').


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
		yield SIGNS[minus]


def _int_part(num: int, step: int = 0) -> Words_T:
	mult_data = MULTS_DATA[step]
	if step+1 < len(MULTS_DATA):
		diff_mult = BASE ** (MULTS_DATA[step+1].pow - mult_data.pow)
		q, r = divmod(num, diff_mult)
	else:
		# Very big number encountered. Process rest with known multipliers.
		# For example, if we know only power 3 ('тысяча'), then in the end for
		# number 101_101_101_000 we will get something like this:
		# 'сто одна тысяча сто один тысяч сто один тысяч'
		q, r = 0, num

	if q:
		yield from _int_part(q, step+1)

	# Difference in neighbour's powers are not necessary equal to 3.
	# For example, if we know only power 3 ('тысяча') and power 9 ('миллиард'),
	# then in the end for number 101_101_101_000 we will get something like this:
	# 'сто один миллиард сто одна тысяча сто один тысяч'
	if r < 1000:
		yield from _before1000(r, step)
	else:
		yield from _int_part(r)

	if r:
		yield mult_data.make_mult_str(r)


def _before20(num: int, step: int) -> Words_T:
	assert 0 <= num < 20
	if num == 0:
		return

	# Special case here.
	# It would be better to generalize this login (and move it to db) if
	# one wants to implement more 'special' cases like this. But since there
	# is only one such simple case at this time, lets keep it here.
	if step == 1:  # thousands
		if num == 1:
			yield 'одна'
		elif num == 2:
			yield 'две'
		else:
			yield BASIC_WORDS[num]
		return

	yield BASIC_WORDS[num]


def _before100(num: int, step: int) -> Words_T:
	assert 0 <= num < 100
	if num < 20:
		yield from _before20(num, step)
		return

	r = num % BASE
	yield BASIC_WORDS[num - r]
	yield from _before20(r, step)


def _before1000(num: int, step: int) -> Words_T:
	assert 0 <= num < 1000
	if num < 100:
		yield from _before100(num, step)
		return

	r = num % BASE2
	yield BASIC_WORDS[num - r]
	yield from _before100(r, step)


def _simple_convert(num: Num_T) -> Tuple[int]:
	"""Convert number to some kind of powers representations.


	"""
	assert num > 0

	return tuple(_simple_int_part(num))


def _simple_int_part(num: int, step: int = 0) -> Iterable[int]:
	p = MULTS_DATA[step].pow
	if step+1 < len(MULTS_DATA):
		diff_mult = BASE ** (MULTS_DATA[step+1].pow - p)
		q, r = divmod(num, diff_mult)
	else:
		q, r = 0, num

	if q:
		yield from _simple_int_part(q, step+1)

	if r < 1000:
		if r:
			yield 0
	else:
		yield from _simple_int_part(r)

	if r:
		if p:
			yield p
