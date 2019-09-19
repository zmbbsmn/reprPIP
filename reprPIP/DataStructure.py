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

    def __init__(self, ohlc: OHLCPoint, direction: Direction):
        self.__ohlc = ohlc
        self.__direction = direction

    @property
    def ohlc(self):
        return self.__ohlc

    @property
    def direction(self):
        return self.__direction

    @property
    def instant(self):
        return self.__ohlc.instant


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

    
