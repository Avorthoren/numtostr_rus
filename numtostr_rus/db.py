from typing import NamedTuple, Callable, Iterable, Sequence, Optional

# Decimal base
BASE = 10
BASE2 = BASE * BASE
# Power, to which conversion algorithm is simple
SIMPLE_POW = 3
SIMPLE_MULT = BASE ** SIMPLE_POW

SIGNS = 'плюс', 'минус'


BASIC_WORDS = {
	0: "ноль",
	1: "один",
	2: "два",
	3: "три",
	4: "четыре",
	5: "пять",
	6: "шесть",
	7: "семь",
	8: "восемь",
	9: "девять",
	10: "десять",
	11: "одиннадцать",
	12: "двенадцать",
	13: "тринадцать",
	14: "четырнадцать",
	15: "пятнадцать",
	16: "шестнадцать",
	17: "семнадцать",
	18: "восемнадцать",
	19: "девятнадцать",
	20: "двадцать",
	30: "тридцать",
	40: "сорок",
	50: "пятьдесят",
	60: "шестьдесят",
	70: "семьдесят",
	80: "восемьдесят",
	90: "девяносто",
	100: "сто",
	200: "двести",
	300: "триста",
	400: "четыреста",
	500: "пятьсот",
	600: "шестьсот",
	700: "семьсот",
	800: "восемьсот",
	900: "девятьсот",
}


MultStrMaker_T = Callable[[Optional[int]], str]


class MultData(NamedTuple):
	pow: int  # means this objects represents mult BASE**pow
	make_mult_str: MultStrMaker_T


def make_thousands_str(num: int = None) -> str:
	assert num is None or 0 <= num < SIMPLE_MULT
	# If we know only thousands, then, for example, number 21000_000 will be
	# converted to 'двадцать одна тысяча тысяч', and for first multiplier this
	# function will be called as ...(21), but second - ...(None).
	if num is None:
		return 'тысяч'

	r2 = num % BASE2
	q, r = divmod(r2, BASE)

	# num: '^\d?[02-9]1$'
	if q != 1 and r == 1:
		return 'тысяча'

	# num: '^\d?[02-9][2-4]$'
	if q != 1 and r in (2, 3, 4):
		return 'тысячи'

	return 'тысяч'


# General case for other multipliers.
def make_make_mult_str(mult_base_str: str) -> MultStrMaker_T:
	def _make_mult_str(num: int = None) -> str:
		assert num is None or 0 <= num < SIMPLE_MULT
		# If we know only thousands and millions, then, for example, number
		# 21_000_000_000_000 will be converted to
		# 'двадцать один миллион миллионов', and for first multiplier this
		# function will be called as ...(21), but second - ...().
		if num is None:
			return f'{mult_base_str}ов'  # 'миллионов'/'миллиардов'

		r2 = num % BASE2
		q, r = divmod(r2, BASE)

		# num: '^\d?[02-9]1$'
		if q != 1 and r == 1:
			return mult_base_str         # 'миллион'/'миллиард'

		# num: '^\d?[02-9][2-4]$'
		if q != 1 and r in (2, 3, 4):
			return f'{mult_base_str}а'   # 'миллиона'/'миллиарда'

		return f'{mult_base_str}ов'      # 'миллионов'/'миллиардов'

	return _make_mult_str


BASIC_MULTS_DATA = (
	MultData(0, lambda *args, **kwargs: ''),
	MultData(SIMPLE_POW, make_thousands_str)
)


# Short scale multipliers data.
# There must be at least two elements in this tuple.
# MultData must have non-negative int `pow`.
# First element must have zero `pow`.
# Second element must have `SIMPLE_POW` `pow`.
# Each next element must have `pow` strictly greater than previous.
# TODO: make it tuple.
SS_MULTS_DATA = [
	# Required elements.
	*BASIC_MULTS_DATA,
	# Optional elements.
	# MultData(6, make_make_mult_str('миллион')),
	MultData(9, make_make_mult_str('миллиард')),
	# MultData(12, make_make_mult_str('триллион')),
	MultData(15, make_make_mult_str('квадриллион')),
	# MultData(18, make_make_mult_str('квинтиллион')),
	# MultData(21, make_make_mult_str('секстиллион')),
	# MultData(24, make_make_mult_str('септиллион')),
	# MultData(27, make_make_mult_str('октиллион')),
	# MultData(30, make_make_mult_str('нониллион')),
	# MultData(33, make_make_mult_str('дециллион')),
	# MultData(36, make_make_mult_str('ундециллион')),
	# MultData(39, make_make_mult_str('дуодециллион')),
	# MultData(42, make_make_mult_str('тредециллион')),
	# MultData(45, make_make_mult_str('кваттордециллион')),
	# MultData(48, make_make_mult_str('квиндециллион')),
	# MultData(51, make_make_mult_str('сексдециллион')),
	# MultData(54, make_make_mult_str('септендециллион')),
	# MultData(57, make_make_mult_str('октодециллион')),
	# MultData(60, make_make_mult_str('новемдециллион')),
	# MultData(63, make_make_mult_str('вигинтиллион')),
	# MultData(66, make_make_mult_str('унвигинтиллион')),
	# MultData(69, make_make_mult_str('дуовигинтиллион')),
	# MultData(72, make_make_mult_str('тревигинтиллион')),
	# MultData(75, make_make_mult_str('кваттуорвигинтиллион')),
	# MultData(78, make_make_mult_str('квинвигинтиллион')),
	# MultData(81, make_make_mult_str('сексвигинтиллион')),
	# MultData(84, make_make_mult_str('септенвигинтиллион')),
	# MultData(87, make_make_mult_str('октовигинтиллион')),
	# MultData(90, make_make_mult_str('новемвигинтиллион')),
	# MultData(93, make_make_mult_str('тригинтиллион')),
	# MultData(96, make_make_mult_str('унтригинтиллион')),
	# MultData(99, make_make_mult_str('дуотригинтиллион')),
	# MultData(102, make_make_mult_str('третригинтиллион')),
	# MultData(105, make_make_mult_str('кваттуортригинтиллион')),
	# MultData(108, make_make_mult_str('квинтригинтиллион')),
	# MultData(111, make_make_mult_str('секстригинтиллион')),
	# MultData(114, make_make_mult_str('септентригинтиллион')),
	# MultData(117, make_make_mult_str('октотригинтиллион')),
	# MultData(120, make_make_mult_str('новемтригинтиллион')),
	# MultData(123, make_make_mult_str('квадрагинтиллион')),
	# MultData(303, make_make_mult_str('центиллион')),
]


# Prefixes of long scale multipliers names that have 'consecutive' powers:
# (6, 9), (12, 15), (18, 21), ...
# See `_long_scale_mults_data` for clarification.
_LS_MULT_NAMES = (
	'м', 'б', 'тр', 'квадр', 'квинт',                                             # 6..33
	'секст', 'септ', 'окт', 'нон', 'дец',                                         # 36..63
	'ундец', 'дуодец', 'тредец', 'кваттордец', 'квиндец',                         # 66..93
	'сексдец', 'септендец', 'октодец', 'новемдец', 'вигинт',                      # 96..123
	'унвигинт', 'дуовигинт', 'тревигинт', 'кваттуорвигинт', 'квинвигинт',         # 126..153
	'сексвигинт', 'септенвигинт', 'октовигинт', 'новемвигинт', 'тригинт',         # 156..183
	'унтригинт', 'дуотригинт', 'третригинт', 'кваттуортригинт', 'квинтригинт',    # 186..213
	'секстригинт', 'септентригинт', 'октотригинт', 'новемтригинт', 'квадрагинт',  # 216..243
	# 'цент' will be added separately below.
)


def _ls_mults_data(mult_names: Iterable[str], start_power_index: int) -> Iterable[MultData]:
	for power_index, mult_name in enumerate(mult_names, start_power_index):
		yield MultData(power_index * 6, make_make_mult_str(f'{mult_name}иллион'))
		yield MultData(power_index * 6 + 3, make_make_mult_str(f'{mult_name}иллиард'))


# Long scale multipliers data.
LS_MULTS_DATA = (
	# Required elements.
	*BASIC_MULTS_DATA,
	# Optional elements.
	*_ls_mults_data(_LS_MULT_NAMES, start_power_index=1),
	# Special mults:
	*_ls_mults_data(mult_names=('цент',), start_power_index=100),
)


def _check_integrity(mults_data: Sequence[MultData]) -> None:
	assert len(mults_data) > 1
	assert mults_data[0].pow == 0
	assert mults_data[1].pow == SIMPLE_POW
	assert all(
		# TODO: add constraint 'all powers are multiples of 3'?
		isinstance(mults_data[i].pow, int) and mults_data[i].pow > mults_data[i-1].pow
		for i in range(1, len(mults_data))
	)


_check_integrity(SS_MULTS_DATA)
_check_integrity(LS_MULTS_DATA)


def main():
	pass


if __name__ == "__main__":
	main()
