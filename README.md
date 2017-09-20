# Struct++

## Introduction

A 100% drop in replacement for the python `struct` module that adds support
for decoding binary structures into namedtuples and decoding bitfields and
other types such as fixed point numbers.

The two main use cases for `structpp` are:

- Naming the results from `struct.unpack` 
- Decoding bitfields

## Basic Usage

### Naming Results

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

You can freely mix name based and index based accessed when using the default namedtuple output:

```python
unpacked = structpp.unpack("<H{val1}H{val2}", packed)
assert unpacked.val1 == 0xFFAB
assert unpacked[1] == 1
```

### Decoding Bitfields

Using the same packed structure as above, we can decode the first 16-bit value into three
values of width 4, 4, and 8 bits:

```python
packed = struct.pack("<HH", 0xFFAB, 1)
unpacked = structpp.unpack("<H{val1: 4, val2: 4, val3: 8}H{val4}", packed)
assert unpacked.val1 == 0xB
assert unpacked.val2 == 0xA
assert unpacked.val3 == 0xFF
assert unpacked.val4 == 1
```

