import random
from typing import Tuple

from src.numtostr_rus import convert, db, converter


# TODO: add tests.


def process(num: int, show: bool = False, hide: bool = False) -> None:
	powers = converter._simple_convert(num)
	if not hide:
		print(f"{powers}: {convert(num)};")
		if show:
			print(f"{num:_}")

	# Две тысячи миллиардов миллиардов миллиардов нониллионов нониллионов
	# Пятьсот миллиардов миллиардов нониллионов нониллионов
	# Двадцать тысяч миллиардов нониллионов нониллионов
	# Сорок миллиардов нониллионов нониллионов
	# Восемьдесят тысяч миллиардов миллиардов нониллионов
	# Четыре тысячи миллиардов нониллионов
	# 2500_000020040_000000000   000_000080000_000004000_000000000   000_000000000_000000000_000000000
	# 2500000020040000000000000000000000000084000000000000000000000000000000000000000000

	mun = converter._convert_backward_from_simple(powers)
	assert num == mun


if __name__ == "__main__":
	"""
	alias направляет на скрипт
	выполнить исходную команду || exit 1
	убедиться, что это нужная подкоманда
	...
	в зависимости от того, init это, или clone, из соответствующего скрипта
	получить конечную директорию
	
	"""

	# S, B, Q = 10**3, 10**9, 10**15
	# process((5 * Q + 5 * S * B))
	# process((5 * Q + 5 * S) * B)
	# process(5 * S * B)
	#
	# print()
	# process((5 * Q + 5 * S * B) * B)
	# process((5 * Q + 5 * S) * B * B)
	# process(5 * S * B * B)
	#
	# print()
	# process((5 * Q + 5 * S * B) * Q * Q)
	# process((5 * Q + 5 * S) * B * Q * Q)
	# process((5 * Q + 5 * S))
	# process(5 * S * B * Q * Q)
	#
	# print()
	# process(((5 * Q + 5 * S * B) * Q + 5 * S * B), show=True)
	# process(((5 * Q + 5 * S) * B * Q + 5 * S * S), show=True)
	#
	# print()
	db.MULTS_DATA[-1] = db.MultData(30, db.make_make_mult_str('нониллион'))
	# S, B, N = 10**3, 10**9, 10**31
	# process((5 * N + 5 * S * B) * N * N)
	# process((5 * N + 5 * S) * B * N * N)
	# process((5 * N + 5 * S))
	# process(5 * S * B * N * N)
	# process((5 * B + 5 * S) * B * B * N * N)

	random.seed(42)
	for e in range(1000_000_000):
		length = random.randint(1, 100)
		num_str = ''.join(
			str(random.randint(1, 9) if (i == 0 or random.random() < 0.05) else 0)
			for i in range(length)
		)
		num = int(num_str)
		# minus = random.randint(0, 1)
		# if minus:
		# 	num = -num
		# print(f"{num:_}: {convert(num)};")
		if e < 10:
			process(num)
		else:
			process(num, show=False, hide=True)
