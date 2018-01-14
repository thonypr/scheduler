# -*- coding: utf-8 -*-

from enum import Enum




class States(Enum):
    S_START = "0"  # Начало нового диалога
    S_ENTER_TRANSPORT = "1"
    S_ENTER_ROUTE = "2"
    S_ENTER_DIRECTION = "3"
    S_ENTER_STOP = "4"
