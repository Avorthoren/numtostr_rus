from typing import NamedTuple, Callable


BASE = 10
BASE2 = BASE * BASE
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

MultStrMaker_T = Callable[[int], str]


class MultData(NamedTuple):
	pow: int  # means this objects represents mult BASE**pow
	make_mult_str: MultStrMaker_T


def make_thousands_str(num: int) -> str:
	assert num >= 0
	if num >= 1000:
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
	def _make_mult_str(num: int) -> str:
		assert num >= 0
		if num >= 1000:
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


# There must be at least two elements in this tuple.
# MultData must have non-negative int `pow`.
# First MultData must have zero `pow`.
# Each next MultData must have `pow` strictly greater than previous.
MULTS_DATA = [
	MultData(0, lambda *args: ''),
	MultData(3, make_thousands_str),
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
	# MultData(303, make_make_mult_str('центеллион')),
]

assert len(MULTS_DATA) > 1
assert MULTS_DATA[0].pow == 0
assert all(
	isinstance(MULTS_DATA[i].pow, int) and MULTS_DATA[i].pow > MULTS_DATA[i-1].pow
	for i in range(1, len(MULTS_DATA))
)
