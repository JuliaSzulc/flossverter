"""
Helper functions for computing distance between colors.
"""
from typing import Optional, Sequence


def squared_euclidean(
    first: Sequence, second: Sequence, weights: Optional[Sequence] = None
) -> float:
    """
    Calculates the sum of squared differences of two lists/arrays.

    If a vector of weights is passed it multiplies each squared difference by the
    corresponding weight.

    Args:
        first (Sequence): List or array of coordinates.
        second (Sequence): List or array of coordinates.
        weights (Optional[Sequence], optional): Optional list or array of weights.
            Defaults to None.

    Returns:
        float: Squared distance between the two given points.
    """
    if not weights:
        weights = [1] * len(first)

    dist_sq = sum([w * (f - s) ** 2 for w, f, s in zip(weights, first, second)])

    return dist_sq
