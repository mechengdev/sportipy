

def ms_to_min_per_km(value: float) -> float:
    """Convert meter per second to minutes per kilometer.

    NOTE: Negative values are not allowed.
    """
    if value < 0:
        raise ValueError("Speed cannot be negative")
    try:
        return 60 / (value * 3.6)
    except ZeroDivisionError:
        return value
