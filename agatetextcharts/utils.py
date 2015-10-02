#!/usr/bin/env python

from decimal import ROUND_CEILING, ROUND_FLOOR

def round_limit(n):
    """
    Round a axis minimum or maximum to a suitable break point.
    """
    magnitude = n.copy_abs().log10().to_integral_exact(rounding=ROUND_FLOOR)
    fraction = (n / (10 ** magnitude))

    limit = fraction.to_integral_exact(rounding=ROUND_CEILING) * (10 ** magnitude)

    # If value fits within a half magnitude, break there
    # if (fraction % 1 < 0.5):
    #     limit -= (10 ** magnitude) / 2

    return limit
    
