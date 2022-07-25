import random
import time

from numtostr_rus import db, converter
from numtostr_rus import convert

# TODO: add 'normal' tests.


def process(num: int, show: bool = False, hide: bool = False) -> None:
	abs_num = abs(num)
	powers = converter._simple_convert(abs_num)
	if not hide:
		if show:
			print(f"{num:_}")
		print(f'{powers}')
		print(f'{convert(num)}')
		print()

	mun = converter._convert_backward_from_simple(powers)
	assert abs_num == mun


def random_tests():
	random.seed(42)
	for e in range(100_000):
		# Generate random string of digits.
		length = random.randint(1, 70)
		num_str = ''.join(
			str(random.randint(1, 9) if (i == 0 or random.random() < 0.5) else 0)
			for i in range(length)
		)
		# Convert it to int.
		num = int(num_str)
		minus = random.randint(0, 1)
		if minus:
			num = -num

		if e < 10:
			# Log first few entries.
			process(num, show=True)
		else:
			process(num, hide=True)

	print("SUCCESS")


def main():
	time0 = time.perf_counter()

	random_tests()

	time1 = time.perf_counter()
	print(f'{time1 - time0} s')


if __name__ == "__main__":
	main()
