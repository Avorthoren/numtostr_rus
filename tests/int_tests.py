import random
from typing import Tuple

from src.numtostr_rus import convert


# TODO: add tests.


# def from_pows_to_num(pows: Tuple[int]) -> int:


from src.numtostr_rus.converter import _simple_convert


def process(num: int) -> None:
	print(f"{_simple_convert(num)}: {convert(num)};")


if __name__ == "__main__":

	S, B, Q = 10**3, 10**9, 10**15
	process((5 * Q + 5 * S * B) * Q * Q)
	process((5 * Q + 5 * S) * B * Q * Q)
	process((5 * Q + 5 * S))
	process(5 * S * B * Q * Q)

	print()
	S, B, N = 10**3, 10**9, 10**31
	process((5 * N + 5 * S * B) * N * N)
	process((5 * N + 5 * S) * B * N * N)
	process((5 * N + 5 * S))
	process(5 * S * B * N * N)
	process((5 * B + 5 * S) * B * B * N * N)


# num = 101_000_000_000
	# print(f"{num:_}: {convert(num)};")
	# num = 101_000_000
	# print(f"{num:_}: {convert(num)};")
	# num = 101_000
	# print(f"{num:_}: {convert(num)};")
	# num = 101_101_000_000
	# print(f"{num:_}: {convert(num)};")
	# num = 101_101_000
	# print(f"{num:_}: {convert(num)};")
	# num = 101_101
	# print(f"{num:_}: {convert(num)};")

	# random.seed(42)
	# for _ in range(100):
	# 	num = random.randint(1000, 10**27)
	# 	minus = random.randint(0, 1)
	# 	if minus:
	# 		num = -num
	# 	print(f"{num:_}: {convert(num)};")
