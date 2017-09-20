"""Ensure that we can properly decode annotated format strings."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import struct
from structpp import unpack


def test_raw_unpacking():
    """Ensure we can unpack unannotated structs."""

    raw = struct.pack("<HH", 0xFFAB, 1)
    out = unpack("<HH", raw)
    out_list = unpack("<HH", raw, aslist=True)
    out_dict = unpack("<HH", raw, asdict=True)

    assert [x for x in out] == [0xFFAB, 1]
    assert out_list == [0xFFAB, 1]
    assert out_dict == {'unnamed_0': 0xFFAB, 'unnamed_1': 1}


def test_named_unpacking():
    """Ensure we can name fields in structs."""

    raw = struct.pack("<HH", 0xFFAB, 1)

    out = unpack("<H{name1}H{name2}", raw)
    out_list = unpack("<H{name1}H{name2}", raw, aslist=True)
    out_dict = unpack("<H{name1}H{name2}", raw, asdict=True)

    assert out.name1 == 0xFFAB
    assert out.name2 == 1
    assert out_list == [0xFFAB, 1]
    assert out_dict == {'name1': 0xFFAB, 'name2': 1}


def test_bitfield_decoding():
    """Ensure we can decode bitfields without names."""

    raw = struct.pack("<HH", 0xFFAB, 1)

    out_list = unpack("<H{:4, :4, :8}H", raw, aslist=True)
    assert out_list == [0xB, 0xA, 0xFF, 1]

def test_named_bitfield_decoding():
    """Ensure we can decode bitfields with names."""

    raw = struct.pack("<HH", 0xFFAB, 1)

    out = unpack("<H{name1:4, name2:4, name3:8}H", raw)

    assert out.name1 == 0xB
    assert out.name2 == 0xA
    assert out.name3 == 0xFF
    assert out[3] == 1
