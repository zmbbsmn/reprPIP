from typeguard import typechecked
from typing import List, Tuple
from .PIPMarker import Instant, PIPMarker, OHLCPoint


@typechecked
def simplify_curve(curve: List[float], static_unit_move: float) -> List[Tuple[int, float]]:

    curve_as_ohlcs = ohlc_dots = [
        OHLCPoint.create_singleton(Instant(i), v) for (i, v) in enumerate(curve)]
    pips, _ = PIPMarker(static_unit_move).walk_through(curve_as_ohlcs)

    return [(p.instant.instant, p.ohlc.c) for p in pips]