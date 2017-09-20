"""Wrapper around struct.unpack."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *  # pylint:disable=C0303,W0401,W0614
import struct
from .format_string import decode_formatstring, create_tuple


def unpack(fmt, packed, asdict=False, aslist=False):
    """Unpack a packed binary struct.

    Args:
        fmt (str): A format string that is compatible with
            struct.unpack with optional annotations enclosed
            in {} that define names and other format information
        packed (bytes): The packed binary data to decode.
        asdict (bool): Optional flag to return a standard python
            dictionary instead of a namedtuple.  This is only
            really useful if all fields are named.
        aslist (bool): Optional flag to return a standard python
            list of results instead of a namedtuple, this is
            mutually exclusive with asdict and both cannot be
            true.

    Returns:
        namedtuple: The decoded data with optional binding of
            named parameters to named properties of the result.
    """

    if asdict and aslist:
        raise ValueError("You cannot specify both asdict and aslist")

    info = decode_formatstring(fmt)
    raw_data = struct.unpack(info.raw_format, packed)

    out = []
    for i, raw in enumerate(raw_data):
        post = info.post_processing[i]
        if post is None:
            out.append(raw)
            continue

        for step in post:
            val = step(raw)
            out.append(val)

    if aslist:
        return out

    if asdict:
        return {x: y for x, y in zip(info.field_names, out)}

    out_tuple = create_tuple(info)
    return out_tuple(*out)
