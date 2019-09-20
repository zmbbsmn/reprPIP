from .DataStructure import *


class PIPMarker:

    def __init__(self, unit_move_distance: float):
        self.__umd = unit_move_distance
        self.__state = PIPState()
        self.__locked_extreme_list = []

    def __calculate(self, ohlc: OHLCPoint):

        units_moved_from_unlocked: float = 0.
        units_moved_from_locked: float = 0.
        if self.__state.is_null_state:
            # give a default state
            start_as_unlocked = ExtremePoint(ohlc, Direction.Down, is_terminal=True)
            start_as_locked = ExtremePoint(ohlc, Direction.Up, is_terminal=True)
            self.__state = PIPState(
                latest_unlocked = start_as_unlocked,
                latest_locked = start_as_locked
            )
            self.__locked_extreme_list.append(start_as_locked)
        else:

            unlocked = self.__state.latest_unlocked
            locked = self.__state.latest_locked

            if unlocked.direction == Direction.Up:
                units_moved_from_unlocked = (ohlc.l - unlocked.extreme_value)/self.__umd
                if units_moved_from_unlocked <= -1: # flipped
                    new_locked = unlocked
                    new_unlocked = ExtremePoint(ohlc, 
                                                Direction.Down, 
                                                units_moved_from_unlocked, 
                                                (ohlc.instant - new_locked.instant).total_seconds())
                    new_state = PIPState(new_unlocked, new_locked, units_moved_from_unlocked)

                    self.__locked_extreme_list.append(new_locked)
                    self.__state = new_state
                elif -1 < units_moved_from_unlocked < 0: # going down but not flipped
                    pass
                else: # continue going up
                    units_moved_from_locked = (ohlc.h - locked.extreme_value)/self.__umd
                    new_unlocked = ExtremePoint(ohlc, 
                                                Direction.Up, 
                                                units_moved_from_locked,
                                                (ohlc.instant - locked.instant).total_seconds())
                    new_state = PIPState(new_unlocked, locked, units_moved_from_locked)
                    self.__state = new_state
            else: # Direction.Down
                units_moved_from_unlocked = (ohlc.h - unlocked.extreme_value)/self.__umd
                if units_moved_from_unlocked >= 1: # flipped
                    new_locked = unlocked
                    new_unlocked = ExtremePoint(ohlc, 
                                                Direction.Up, 
                                                units_moved_from_unlocked,
                                                (ohlc.instant - unlocked.instant).total_seconds())
                    new_state = PIPState(new_unlocked, new_locked, units_moved_from_unlocked)
                    self.__locked_extreme_list.append(new_locked)
                    self.__state = new_state
                elif 0 < units_moved_from_unlocked < 1: # going up but not flipped
                    pass
                else: # continue going down
                    units_moved_from_locked = (ohlc.l - locked.extreme_value)/self.__umd
                    new_unlocked = ExtremePoint(ohlc, 
                                                Direction.Down, 
                                                units_moved_from_locked,
                                                (ohlc.instant - locked.instant).total_seconds())
                    new_state = PIPState(new_unlocked, locked, units_moved_from_locked)
                    self.__state = new_state
        return self.__state.units_moved_on_direction

    def walk_through(self, path: list):
        assert all([type(point)==OHLCPoint for point in path])
        path_ranges = [(point.instant, self.__calculate(point)) 
                        for point in path]

        pips = self.__locked_extreme_list + [self.__state.latest_unlocked]

        return pips, path_ranges