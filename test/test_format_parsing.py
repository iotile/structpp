"""Ensure that the format string annotation parser works correctly."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from structpp.format_string import decode_formatstring


def test_passthrough():
    """Make sure format strings with no annotations parse correctly."""

    out = decode_formatstring("<HBL")
    assert out.prefix == '<'
    assert out.raw_format == "<HBL"
    assert out.field_names == ['unnamed_0', 'unnamed_1', 'unnamed_2']

    out = decode_formatstring("BL")
    assert out.prefix == ''
    assert out.raw_format == "BL"
    assert out.field_names == ['unnamed_0', 'unnamed_1']

    out = decode_formatstring("4BL")
    assert out.prefix == ''
    assert out.raw_format == '4BL'
    assert out.field_names == ['unnamed_0', 'unnamed_1']

    out = decode_formatstring("<H{name}B")
    assert out.prefix == '<'
    assert out.raw_format == "<HB"
