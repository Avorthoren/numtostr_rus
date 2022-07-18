import random

from src.numtostr_rus import convert


# TODO: add tests.


if __name__ == "__main__":
	random.seed(42)
	for _ in range(100):
		num = random.randint(100, 999)
		minus = random.randint(0, 1)
		if minus:
			num = -num
		print(num, convert(num))
