from itertools import chain, repeat
from typing import MutableSequence, Tuple, Iterable, Sequence, Iterator

from numtostr_rus import db


# Currently all powers of multipliers for both long and short scales are
# multiples of 3. But let's not rely on this fact and implement more general
# logic.
class AnchorMult:
	def __init__(self, mults: Tuple[db.MultData, ...]):
		self.mults = mults
		self._pow = sum(mult.pow for mult in mults)

	__slots__ = 'mults', '_pow'

	@property
	def pow(self):
		return self._pow

	def __str__(self):
		return f"({self._pow}={'+'.join(str(mult.pow) for mult in self.mults)})"

	__repr__ = __str__


ZERO_ANCHOR_MULT = AnchorMult((db.BASIC_MULTS_DATA[0],))
SS_ANCHOR_MULTS = []
LS_ANCHOR_MULTS = []


def _fill_anchor_mults(mults_data: Iterable[db.MultData], anchor_mults: MutableSequence[AnchorMult]):
	mults_data_it = iter(mults_data)
	# Consume zero power mult.
	next(mults_data_it)
	# Consume a thousand.
	prev_mult_data = next(mults_data_it)
	anchor_mults.append(AnchorMult(
		(prev_mult_data,)
	))
	# Process all other multipliers.
	for mult_data in mults_data_it:
		for i, anchor_mult in enumerate(anchor_mults):
			if prev_mult_data.pow + anchor_mult.pow >= mult_data.pow:
				break
			anchor_mults.append(AnchorMult(
				(*anchor_mult.mults, prev_mult_data)
			))

		anchor_mults.append(AnchorMult(
			(mult_data,)
		))
		prev_mult_data = mult_data


_fill_anchor_mults(db.SS_MULTS_DATA, SS_ANCHOR_MULTS)
_fill_anchor_mults(db.LS_MULTS_DATA, LS_ANCHOR_MULTS)


def get_mults(
	anchor_mults: Sequence[AnchorMult],
	step_q: int,
	step_r: int
) -> Iterator[db.MultData]:
	"""Get mults of `step_q * len(anchor_mults) + step_r`-th anchor."""
	assert 0 <= step_r < len(anchor_mults)
	# Special case.
	# It will yield empty string, but just for uniformity...
	if not step_q and not step_r:
		return iter(ZERO_ANCHOR_MULT.mults)

	last_mult = anchor_mults[-1].mults[0]
	repeat_mults = repeat(last_mult, step_q)
	if not step_r:
		return repeat_mults

	anchor_mult = anchor_mults[step_r - 1]
	return chain(anchor_mult.mults, repeat_mults)


def main():
	for anchor_mult in SS_ANCHOR_MULTS:
		print(anchor_mult)


if __name__ == "__main__":
	main()
