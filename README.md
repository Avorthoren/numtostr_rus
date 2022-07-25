# Simple python number-to-russian-string converter.

[![image](https://img.shields.io/pypi/v/numtostr_rus.svg)](https://python.org/pypi/numtostr_rus)
[![image](https://img.shields.io/pypi/pyversions/numtostr_rus.svg)](https://python.org/pypi/numtostr_rus)
[![image](https://img.shields.io/badge/license-MIT-lightgrey)](https://python.org/pypi/numtostr_rus)
[![image](https://img.shields.io/pypi/dm/numtostr_rus)](https://github.com/Avorthoren/numtostr_rus)

Current version works only for ints.<br />
Requires python version 3.6.2 or higher.

## Examples:

```pycon
>>> import numtostr_rus
>>>
>>> numtostr_rus.convert(0)
'ноль'

>>> numtostr_rus.convert(-508)
'минус пятьсот восемь'

>>> numtostr_rus.convert(600)
'шестьсот'

>>> numtostr_rus.convert(
...     42 * 10**606 + 73 * 10**177
... )
'сорок два центиллиона центиллионов семьдесят три септендециллиона квадрагинтиллионов'

```
