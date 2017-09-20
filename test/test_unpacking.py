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
