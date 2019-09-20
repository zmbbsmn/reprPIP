from enum import IntEnum
from datetime import datetime


class Direction:
    Up = 1
    Down = -1


class OHLCPoint:

    def __init__(self, instant: datetime, o: float, h: float, l: float, c: float):
        self.__instant = instant
        self.__o = o
        self.__h = h
        self.__l = l
        self.__c = c

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
    def create_singleton(instant: datetime, value: float):
        singleton = OHLCPoint(instant, value, value, value, value)
        return singleton


class ExtremePoint:

    def __init__(self,
                 ohlc: OHLCPoint, 
                 direction: Direction, 
                 vertical_move_since: float = None,
                 horizontal_move_since: float = None):
        self.__ohlc = ohlc
        self.__direction = direction
        self.__vertical_move_since = vertical_move_since
        self.__horizontal_move_since = horizontal_move_since

    @property
    def ohlc(self):
        return self.__ohlc

    @property
    def direction(self):
        return self.__direction

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
        if self.__direction == Direction.Up:
            str_direction = '⬈'
        else:
            str_direction = '︎︎︎⬊'

        str_vert_move = '*[{0},{0}]'.format(self.__vertical_move_since)
        str_hori_move = '~[{0},{0}]'.format(self.__horizontal_move_since)

        return str_direction + str_vert_move + str_hori_move


class PIPState:

    def __init__(self, latest_unlocked: ExtremePoint = None, latest_locked: ExtremePoint = None):
        self.__latest_unlocked = latest_unlocked
        self.__latest_locked = latest_locked

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

    
