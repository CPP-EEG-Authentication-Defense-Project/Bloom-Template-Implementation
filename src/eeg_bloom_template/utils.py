import typing


C = typing.TypeVar('C', bound=typing.Collection)


def iter_ratio_slices(iterable_data: C, slice_ratio: float) -> typing.Iterator[C]:
    """
    Iterate over a given collection of data using the given ratio to define the proportional size of each slice
    to be yielded.

    :param iterable_data: The collection to iterate over by slices.
    :param slice_ratio: The proportional size of the slices.
    :returns: An iterator over the slices of the given collection of data.
    """
    if not 0 < slice_ratio <= 1:
        raise ValueError(f'Slice ratio must be between 0 and 1, upper bound inclusive (got {slice_ratio}).')
    iterable_length = len(iterable_data)
    slice_size = int(slice_ratio * iterable_length)

    for i in range(0, iterable_length, slice_size):
        slice_end = min(i + slice_size, iterable_length)
        yield iterable_data[i:slice_end]


def convert_unsigned_128_to_signed(unsigned_128: int) -> int:
    """
    Converts a given unsigned 128-bit integer into a signed 128-bit integer, wrapping around into negative
    values if the unsigned value overflows.

    :param unsigned_128: The unsigned 128-bit integer value.
    :returns: A signed 128-bit integer value.
    """
    max_signed = 2**127 - 1
    signed_value = unsigned_128 & max_signed

    if unsigned_128 & (1 << 127):
        signed_value = -(signed_value ^ max_signed) - 1

    return signed_value
