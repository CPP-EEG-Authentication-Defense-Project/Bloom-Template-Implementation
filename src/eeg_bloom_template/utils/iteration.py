import typing
import math


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
    # If the number is too small, take the ceiling to avoid the slice size being 0
    slice_size_raw = slice_ratio * iterable_length
    if slice_size_raw < 1:
        slice_size = math.ceil(slice_size_raw)
    else:
        slice_size = int(slice_size_raw)

    for i in range(0, iterable_length, slice_size):
        slice_end = min(i + slice_size, iterable_length)
        yield iterable_data[i:slice_end]
