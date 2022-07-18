# Simple python number-to-russian-string-converter.

[![image](https://img.shields.io/pypi/v/numtostr_rus.svg)](https://python.org/pypi/numtostr_rus)
[![image](https://img.shields.io/pypi/pyversions/numtostr_rus.svg)](https://python.org/pypi/numtostr_rus)
[![image](https://img.shields.io/badge/license-MIT-lightgrey)](https://python.org/pypi/numtostr_rus)
[![image](https://img.shields.io/pypi/dm/numtostr_rus)](https://github.com/Avorthoren/numtostr_rus)

Current version works only for ints with abs < 1000.

## Examples:

```pycon
>>> from numtostr_rus import converter as numtostr_rus
>>>
>>> numtostr_rus(
...     0
... )
'ноль'

>>> numtostr_rus(
...     -508
... )
'минус пятьсот восемь'

>>> numtostr_rus(
...     600
... )
'шестьсот'

```
