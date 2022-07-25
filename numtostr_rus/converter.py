from functools import reduce
from itertools import chain, repeat
import operator
from typing import Union, Iterable, Tuple, NamedTuple

from numtostr_rus.db import BASE, BASE2, SIGNS, BASIC_WORDS, SS_MULTS_DATA, SIMPLE_MULT
from numtostr_rus.mult import SS_ANCHOR_MULTS, LS_ANCHOR_MULTS, ZERO_ANCHOR_MULT, get_mults


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
	assert num
	zero_anchor_mult = ZERO_ANCHOR_MULT
	anchor_mults = SS_ANCHOR_MULTS

	step_q, step_r = divmod(step, len(anchor_mults))

	next_pow = anchor_mults[step_r].pow
	anchor_mult = anchor_mults[step_r-1] if step_r else zero_anchor_mult
	curr_pow = anchor_mult.pow
	diff_mult = BASE ** (next_pow - curr_pow)
	q, r = divmod(num, diff_mult)

	if q:
		# Left part of the number.
		yield from _int_part(q, step+1)

	# Anchor system guarantees that at this point `r < SIMPLE_MULT`.
	if r:
		# Current part of the number.
		yield from _before1000(r, step_r)
		# Multipliers.
		mults = get_mults(anchor_mults, step_q, step_r)
		for i, mult_data in enumerate(mults):
			yield mult_data.make_mult_str(None if i else r)


def _before20(num: int, step: int) -> Words_T:
	assert 0 <= num < 2 * BASE
	if num == 0:
		return

	# Special case here.
	# It would be better to generalize this case (and move it to db) if
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
	assert 0 <= num < BASE2
	if num < 2 * BASE:
		yield from _before20(num, step)
		return

	r = num % BASE
	yield BASIC_WORDS[num - r]
	yield from _before20(r, step)


def _before1000(num: int, step: int) -> Words_T:
	assert 0 <= num < SIMPLE_MULT
	if num < BASE2:
		yield from _before100(num, step)
		return

	r = num % BASE2
	yield BASIC_WORDS[num - r]
	yield from _before100(r, step)


class Mult(NamedTuple):
	power: int
	mult: int = 1

	def __str__(self):
		return f"{self.power}{'' if self.mult == 1 else f':{self.mult}'}"

	__repr__ = __str__

	def construct(self) -> int:
		return self.mult * (BASE ** self.power)


def _simple_convert(num: Num_T) -> Tuple[Mult]:
	"""Convert number to some kind of powers representations.
	Mimics `convert` but uses powers (as ints) instead of words, and glues
	them into tuple.
	May be used in the future to do backward conversion from string to number.
	TODO: implement num <= 0.
	"""
	assert num > 0

	return tuple(_simple_int_part(num))


def _simple_int_part(num: int, step: int = 0) -> Iterable[Mult]:
	"""See `_int_part` implementation for explanations."""
	p = SS_MULTS_DATA[step].pow
	if step+1 < len(SS_MULTS_DATA):
		diff_mult = BASE ** (SS_MULTS_DATA[step + 1].pow - p)
		q, r = divmod(num, diff_mult)
	else:
		q, r = 0, num

	if q:
		yield from _simple_int_part(q, step+1)

	if r < SIMPLE_MULT:
		if r:
			yield Mult(0, r)
	else:
		yield from _simple_int_part(r)

	if r:
		if p:
			yield Mult(p)


def _convert_backward_from_simple(powers: Tuple[Mult], left: int = 0, right: int = None) -> int:
	assert powers
	assert powers[left].power == 0

	if right is None:
		right = len(powers)

	max_left_pow = [0]
	for i in range(left + 1, right):
		max_left_pow.append(max(powers[i-1].power, max_left_pow[-1]))

	# Find common multiplier.
	# Since `powers[left].power == 0`, minimum value of `cmi` is `left+1`.
	cmi = right
	while powers[cmi - 1].power >= max_left_pow[cmi - 1 - left] > 0:
		cmi -= 1
	# Calculate it.
	common_mult = reduce(
		operator.mul,
		(powers[i].construct() for i in range(cmi, right)),
		1
	)

	# Find rightmost simple chain left of common multiplier.
	sci = cmi - 1
	while powers[sci].power:
		sci -= 1
	# Calculate it.
	middle_part = reduce(
		operator.mul,
		(powers[i].construct() for i in range(sci, cmi)),
		1
	)
	# middle_part = _convert_backward_from_simple(powers, sci, cmi)

	# Calculate rest.
	left_part = _convert_backward_from_simple(powers, left, sci) if left < sci else 0

	return (left_part + middle_part) * common_mult


def main():
	print(convert(42*10**39 + 101*10**18 + 10**15 + 3*10**12))


if __name__ == "__main__":
	main()

