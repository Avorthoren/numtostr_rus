from functools import reduce
from itertools import chain
import operator
from typing import Union, Iterable, Tuple, NamedTuple

from numtostr_rus import db, mult


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
#       CUSTOM: ...

# TODO: implement capitalize flag for capitalizing first word.

# TODO: implement max_step to specify max multiplier (like 'миллиард').


def convert(num: Num_T) -> str:
	"""Main function of the package.
	Converts `num` to russian words representation.
	Only for int -1000 < num < 1000.
	"""
	if num == 0:
		return db.BASIC_WORDS[0]

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
		yield db.SIGNS[minus]


def _int_part(num: int, step_q: int = 0, step_r: int = 0) -> Words_T:
	assert num
	anchor_mults = mult.SS_ANCHOR_MULTS
	# Total step is `step_q * len(anchor_mults) + step_r`.
	assert 0 <= step_r < len(anchor_mults)

	next_pow = anchor_mults[step_r].pow
	curr_pow = anchor_mults[step_r - 1].pow if step_r else 0
	diff_mult = db.BASE ** (next_pow - curr_pow)
	q, r = divmod(num, diff_mult)

	if q:
		# Left part of the number.
		if step_r + 1 < len(anchor_mults):
			new_step_q, new_step_r = step_q, step_r + 1
		else:
			new_step_q, new_step_r = step_q + 1, 0
		yield from _int_part(q, new_step_q, new_step_r)

	# Anchor system guarantees that at this point `r < SIMPLE_MULT`.
	if r:
		mults = mult.get_mults(anchor_mults, step_q, step_r)
		first_mult = next(mults)
		# Current part of the number.
		yield from _before1000(r, first_mult)
		# Multipliers.
		yield first_mult.make_mult_str(r)
		for mult_data in mults:
			yield mult_data.make_mult_str()


def _before20(num: int, first_mult: db.MultData) -> Words_T:
	assert 0 <= num < 2 * db.BASE
	if num == 0:
		return

	# Special case here.
	# It would be better to generalize this case (and move it to db) if
	# one wants to implement more 'special' cases like this. But since there
	# is only one such simple case at this time, lets keep it here.
	if first_mult.pow == db.SIMPLE_POW:  # thousands
		if num == 1:
			yield 'одна'  # 'тысяча'
		elif num == 2:
			yield 'две'   # 'тысячи'
		else:
			yield db.BASIC_WORDS[num]
		return

	yield db.BASIC_WORDS[num]


def _before100(num: int, first_mult: db.MultData) -> Words_T:
	assert 0 <= num < db.BASE2
	if num < 2 * db.BASE:
		yield from _before20(num, first_mult)
		return

	r = num % db.BASE
	yield db.BASIC_WORDS[num - r]
	yield from _before20(r, first_mult)


def _before1000(num: int, first_mult: db.MultData) -> Words_T:
	assert 0 <= num < db.SIMPLE_MULT
	if num < db.BASE2:
		yield from _before100(num, first_mult)
		return

	r = num % db.BASE2
	yield db.BASIC_WORDS[num - r]
	yield from _before100(r, first_mult)


class Mult(NamedTuple):
	pow: int
	mult: int = 1

	def __str__(self):
		return f"{self.pow}{'' if self.mult == 1 and self.pow else f':{self.mult}'}"

	__repr__ = __str__

	def construct(self) -> int:
		return self.mult * (db.BASE ** self.pow)


def _simple_convert(num: Num_T) -> Tuple[Mult]:
	"""Convert number to some kind of powers representations.
	Mimics `convert` but uses powers (as ints) instead of words, and glues
	them into tuple.
	May be used in the future to do backward conversion from string to number.
	TODO: implement num <= 0.
	"""
	assert num > 0

	return tuple(_simple_int_part(num))


def _simple_int_part(num: int, step_q: int = 0, step_r: int = 0) -> Iterable[Mult]:
	"""See `_int_part` implementation for explanations."""
	assert num
	anchor_mults = mult.SS_ANCHOR_MULTS
	# Total step is `step_q * len(anchor_mults) + step_r`.
	assert 0 <= step_r < len(anchor_mults)

	next_pow = anchor_mults[step_r].pow
	curr_pow = anchor_mults[step_r - 1].pow if step_r else 0
	diff_mult = db.BASE ** (next_pow - curr_pow)
	q, r = divmod(num, diff_mult)

	if q:
		# Left part of the number.
		if step_r + 1 < len(anchor_mults):
			new_step_q, new_step_r = step_q, step_r + 1
		else:
			new_step_q, new_step_r = step_q + 1, 0
		yield from _simple_int_part(q, new_step_q, new_step_r)

	# Anchor system guarantees that at this point `r < SIMPLE_MULT`.
	if r:
		# Current part of the number.
		yield Mult(0, r)
		# Multipliers.
		if step_q or step_r:
			for mult_data in mult.get_mults(anchor_mults, step_q, step_r):
				yield Mult(mult_data.pow)


def _convert_backward_from_simple(powers: Tuple[Mult]) -> int:
	result = 0
	left, right = 0, 1
	while left < len(powers):
		while right < len(powers) and powers[right].pow:
			right += 1

		result += reduce(
			operator.mul,
			(powers[i].construct() for i in range(left, right))
		)

		left, right = right, right + 1

	return result


def main():
	num = 42 * 10**606 + 73 * 10**177
	print(f'{num:_}')
	print(convert(num))
	print(_simple_convert(abs(num)))


if __name__ == "__main__":
	main()

