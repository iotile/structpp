# Struct++

## Introduction

A 100% drop in replacement for the python `struct` module that adds support
for decoding binary structures into namedtuples and decoding bitfields and
other types such as fixed point numbers.

The two main use cases for `structpp` are:

- Naming the results from `struct.unpack` 
- Decoding bitfields

## Basic Usage

To name the results of an unpacked binary structure, put the name
in curly brackets after the format code:

```python
import struct
import structpp

packed = struct.pack("<HH", 0xFFAB, 1)
unpacked = structpp.unpack("<H{val1}H{val2}", packed)

assert unpacked.val1 == 0xFFAB
assert unpacked.val2 == 1
```

You can also ask for the results as a dictionary or list instead of the default namedtuple:

```python
unpacked = structpp.unpack("<H{val1}H{val2}", packed, asdict=True)
assert unpacked['val1'] == 0xFFAB
assert unpacked['val2'] == 1

unpacked = structpp.unpack("<H{val1}H{val2}", packed, aslist=True)
assert unpacked[0] == 0xFFAB
assert unpacked[1] == 1
```
