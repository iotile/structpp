"""Decode enhancements to the struct format string."""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *  # pylint:disable=C0303,W0401,W0614
from collections import namedtuple

DecoderInfo = namedtuple('DecoderInfo', ['raw_format', 'prefix', 'parsed_format', 'field_names', 'post_processing'])


def decode_formatstring(fmt):
    """Decode an annotated struct format string.

    This function accepts format strings with annotations following
    any character enclosed in { } characters. The contents of the brackets
    should have the following form:

    {[name][:bit_width], [name2][:bit_width]}
    Either name or bit_width may be omitted if not desired.  If name is
    specified, that member will be available as a named member of the created
    named tuple.  If bit_width is specified, the field will be subdivided and
    just those bits will be extracted.

    Args:
        fmt (str): The potentially annotated format string that we are asked to
            decode.

    Returns:
        DecoderInfo: A named tuple containing decoder information that is used
            to perform additional parsing of struct results.
    """

    parsed_format = []
    count = ''
    field_names = []
    post_processing = []
    prefix = ''

    in_annotation = False
    annotation = ''

    if len(fmt) > 0 and not (fmt[0].isalpha() or fmt[0].isdigit()):
        prefix = fmt[0]
        fmt = fmt[1:]

    for char in fmt:
        if char == '}':
            in_annotation = False
            names, steps = decode_annotation(annotation)

            # Remove the old unnamed last entry
            field_names = field_names[:-1]
            for name in names:
                if name != '':
                    field_names.append(name)
                else:
                    field_names.append("unnamed_{}".format(len(field_names)))

            post_processing[-1] = steps
            annotation = ''
            continue
        elif in_annotation:
            annotation += char
            continue
        elif char == '{':
            in_annotation = True
            continue

        if char.isdigit():
            count += char
            continue
        elif char.isalpha():
            parsed_format.append((char, count))
            field_names.append("unnamed_{}".format(len(field_names)))
            post_processing.append(None)
            count = ''

    raw_format = prefix + "".join([count + char for char, count in parsed_format])

    return DecoderInfo(raw_format, prefix, parsed_format, field_names, post_processing)


def decode_annotation(annotation):
    """Decode an annotation into a set of actions and result names.

    Annotations can do one of 3 things:
    - Assign a name to a field
    - split a field into multiple subfields based on bitfield processing
    - Postprocess a value according to some rule

    Returns:
        list, list: A list of all field names that this annotation will result
            in and a list of callables that will produce field values from the
            raw parse result
    """

    subfields = annotation.split(",")

    out_names = []
    out_steps = []

    combined_width = 0

    for field in subfields:
        step = lambda x: x

        name, _sep, bitwidth = field.partition(":")
        name = name.strip()
        bitwidth = bitwidth.strip()

        out_names.append(name)
        if bitwidth != '':
            bitwidth = int(bitwidth)
            step = lambda x, width=bitwidth, combined=combined_width: ((x >> combined) & ((1 << width) - 1))
            combined_width += bitwidth

        out_steps.append(step)

    return out_names, out_steps


def create_tuple(info):
    """Create a namedtuple from the information in info.

    Returns:
        type: a new namedtuple type that can be instantiated.
    """

    return namedtuple('UnnamedTuple', info.field_names)
