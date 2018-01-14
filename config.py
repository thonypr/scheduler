# -*- coding: utf-8 -*-

from enum import Enum

token = u"424882927:AAGKLtBw6ZmZyQQH9mfSKVpztQO6LxzyNX8"


class States(Enum):
    S_START = "0"  # Начало нового диалога
    S_ENTER_TRANSPORT = "1"
    S_ENTER_ROUTE = "2"
    S_ENTER_DIRECTION = "3"
    S_ENTER_STOP = "4"
