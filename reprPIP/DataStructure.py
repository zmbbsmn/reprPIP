from enum import IntEnum
from datetime import datetime
from typeguard import typechecked
from typing import NoReturn, TypeVar, NoReturn, Optional, List


class Instant:

    @typechecked
    def __init__(self, instant: TypeVar('Instant', datetime, int)):
        self.__instant = instant

    @typechecked
    def __sub__(self, other: "Instant") -> float:
        if isinstance(self.instant, datetime) and isinstance(other.instant, datetime):
            return (self.instant - other.instant).total_seconds()
        elif isinstance(self.instant, int) and isinstance(other.instant, int):
            return self.instant - other.instant
        else:
            raise TypeError('TypeError in minus op of Instant')

    @property
    def instant(self):
        return self.__instant

    def __repr__(self):
        return str(self.instant)


class Direction(IntEnum):
    Up = 1
    Down = -1


class OHLCPoint:

    @typechecked
    def __init__(self, instant: Instant, o: float, h: float, l: float, c: float):
        self.__instant = instant
        self.__o = o
        self.__h = h
        self.__l = l
        self.__c = c

    def __repr__(self):
        return 'OHLCPoint(instant:{0}, o:{1}, h:{2}, l:{3}, c:{4})'.format(
            repr(self.__instant),
            repr(self.__o),
            repr(self.__h),
            repr(self.__l),
            repr(self.__c)
        )

    @property
    def o(self):
        return self.__o

    @property
    def h(self):
        return self.__h

    @property
    def l(self):
        return self.__l

    @property
    def c(self):
        return self.__c

    @property
    def instant(self):
        return self.__instant

    @staticmethod 
    @typechecked
    def create_singleton(instant: Instant, value: float) -> "OHLCPoint":
        singleton = OHLCPoint(instant, value, value, value, value)
        return singleton


class ExtremePoint:

    @typechecked
    def __init__(self,
                 ohlc: OHLCPoint, 
                 direction: Direction, 
                 vertical_move_since: Optional[float] = None,
                 horizontal_move_since: Optional[float] = None,
                 is_terminal: bool = False):
        self.__ohlc = ohlc
        self.__direction = direction
        self.__vertical_move_since = vertical_move_since
        self.__horizontal_move_since = horizontal_move_since
        self.__is_terminal = is_terminal

    def __repr__(self):
        return repr(self.__ohlc)

    @property
    def ohlc(self):
        return self.__ohlc

    @property
    def direction(self):
        return self.__direction

    @property
    def extreme_value(self):
        if self.__direction == Direction.Up:
            return self.__ohlc.h
        else:
            return self.__ohlc.l

    @property
    def instant(self):
        return self.__ohlc.instant

    @property
    def vertical_move_since_last_extreme(self):
        return self.__vertical_move_since

    @property
    def horizontal_move_since_last_extreme(self):
        return self.__horizontal_move_since

    def __str__(self):

        if self.__is_terminal:
            return '∙'
        else:
            if self.__direction == Direction.Up:
                str_direction = '⬈'
            else:
                str_direction = '︎︎︎⬊'

            str_vert_move = '*{0}'.format(self.__vertical_move_since)
            str_hori_move = '~{0}'.format(self.__horizontal_move_since)

            return str_direction + str_vert_move + str_hori_move


class PIPState:

    @typechecked
    def __init__(self,
                 latest_unlocked: Optional[ExtremePoint] = None, 
                 latest_locked: Optional[ExtremePoint] = None, 
                 units_moved_on_direction: Optional[float] = None):
        
        self.__latest_unlocked = latest_unlocked
        self.__latest_locked = latest_locked
        self.__move_on_direction = units_moved_on_direction

    @property
    def latest_unlocked(self):
        return self.__latest_unlocked

    @latest_unlocked.setter
    def latest_unlocked(self, extreme_point: ExtremePoint):
        self.__latest_unlocked = extreme_point

    @property
    def latest_locked(self):
        return self.__latest_locked

    @latest_locked.setter
    def latest_locked(self, extreme_point: ExtremePoint):
        self.__latest_locked = extreme_point

    @property
    def is_null_state(self):
        return self.__latest_unlocked is None and self.__latest_locked is None

    @property
    def units_moved_on_direction(self):
        return self.__move_on_direction 

    @units_moved_on_direction.setter
    def units_moved_on_direction(self, units: float):
        self.__move_on_direction = units

    
