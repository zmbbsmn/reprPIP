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
            start_as_extrme = ExtremePoint(ohlc, Direction.Up, units_moved, 0)
            self.__state = PIPState(
                latest_unlocked = start_as_extrme,
                latest_locked = start_as_extrme
            )
            self.__locked_extreme_list.append(ExtremePoint(ohlc, Direction.Up, units_moved, 0))
        else:
            unlocked = self.__state.latest_unlocked
            locked = self.__state.latest_locked

            if unlocked.direction == Direction.Up:
                units_moved = (ohlc.l - unlocked.ohlc.h)/self.__umd
                if units_moved <= -1: # flipped
                    self.__locked_extreme_list.append(unlocked)
                    self.__state = PIPState(
                        latest_unlocked = ExtremePoint(ohlc, 
                                                       Direction.Down, 
                                                       units_moved, 
                                                       (ohlc.instant - unlocked.instant).total_seconds()),
                        latest_locked = self.__state.latest_unlocked
                    )
                elif -1 < units_moved < 0: # going down but not flipped
                    pass
                else: # continue going up
                    self.__state = PIPState(
                        latest_unlocked = ExtremePoint(ohlc, 
                                                       Direction.Up, 
                                                       units_moved,
                                                       (ohlc.instant - locked.instant).total_seconds()),
                        latest_locked = self.__state.latest_locked
                    )
            else: # Direction.Down
                units_moved = (ohlc.h - unlocked.ohlc.l)/self.__umd
                if units_moved >= 1: # flipped
                    self.__locked_extreme_list.append(unlocked)
                    self.__state = PIPState(
                        latest_unlocked = ExtremePoint(ohlc, 
                                                       Direction.Up, 
                                                       units_moved,
                                                       (ohlc.instant - unlocked.instant).total_seconds()),
                        latest_locked = self.__state.latest_unlocked
                    )
                elif 0 < units_moved < 1: # going up but not flipped
                    pass
                else: # continue going down
                    self.__state = PIPState(
                        latest_unlocked = ExtremePoint(ohlc, 
                                                       Direction.Down, 
                                                       units_moved,
                                                       ohlc.instant - locked.instant.total_seconds()),
                        latest_locked = self.__state.latest_locked
                    )
        return units_moved

    def walk_through(self, path: list):
        assert all([type(point)==OHLCPoint for point in path])
        path_ranges = [(idx, self.__calculate(point)) 
                        for idx, point in enumerate(path)]

        pips = self.__locked_extreme_list + [self.__state.latest_unlocked]

        return pips, path_ranges