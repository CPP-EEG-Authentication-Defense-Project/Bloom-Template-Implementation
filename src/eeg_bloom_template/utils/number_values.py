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


def clamp_value(value: int, min_value: int, max_value: int) -> int:
    """
    Clamps a given value between a minimum and a maximum value.

    :param value: The value to clamp.
    :param min_value: The minimum value.
    :param max_value: The maximum value.
    :returns: The clamped value.
    """
    return max(min(max_value, value), min_value)
