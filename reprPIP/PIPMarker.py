from .DataStructure import *


class PIPMarker:

    def __init__(self, unit_move_distance: float):
        self.__umd = unit_move_distance
        self.__state = PIPState()
        self.__locked_extreme_list = []

    def __calculate(self, ohlc: OHLCPoint):

        units_moved: float = 0.
        if self.__state.is_null_state:
            # give a default state
            self.__state = PIPState(
                latest_unlocked=ExtremePoint(ohlc, Direction.Up),
                latest_locked=None
            )
            self.__locked_extreme_list.append(ExtremePoint(ohlc, Direction.Up))
            units_moved = 1.
        else:
            unlocked = self.__state.latest_unlocked
            locked = self.__state.latest_locked

            if unlocked.direction == Direction.Up:
                units_moved = (ohlc.l - unlocked.ohlc.h)/self.__umd
                if units_moved <= -1: # flipped
                    self.__locked_extreme_list.append(unlocked)
                    self.__state = PIPState(
                        latest_unlocked = ExtremePoint(ohlc, Direction.Down),
                        latest_locked = self.__state.latest_unlocked
                    )
                elif -1 < units_moved < 0: # going down but not flipped
                    pass
                else: # continue going up
                    self.__state = PIPState(
                        latest_unlocked = ExtremePoint(ohlc, Direction.Up),
                        latest_locked = self.__state.latest_locked
                    )
            else: # Direction.Down
                units_moved = (ohlc.h - unlocked.ohlc.l)/self.__umd
                if units_moved >= 1: # flipped
                    self.__locked_extreme_list.append(unlocked)
                    self.__state = PIPState(
                        latest_unlocked = ExtremePoint(ohlc, Direction.Up),
                        latest_locked = self.__state.latest_unlocked
                    )
                elif 0 < units_moved < 1: # going up but not flipped
                    pass
                else: # continue going down
                    self.__state = PIPState(
                        latest_unlocked = ExtremePoint(ohlc, Direction.Down),
                        latest_locked = self.__state.latest_locked
                    )
        return units_moved

    def walk_through(self, path: list):
        assert all([type(point)==OHLCPoint for point in path])
        path_ranges = [(idx, self.__calculate(point)) 
                        for idx, point in enumerate(path)]

        pips = [(e.instant, e.ohlc) for e in self.__locked_extreme_list] +\
                [(self.__state.latest_unlocked.instant, self.__state.latest_unlocked.ohlc)]

        return pips, path_ranges