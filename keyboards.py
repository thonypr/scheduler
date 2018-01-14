# -*- coding: utf-8 -*-

from telebot import types
import math
import messages


def get_dimension(count, cols):
    # side = math.sqrt(count)
    # whole = math.trunc(side)
    # return whole + 1
    rows = int(math.trunc(count/cols))+1
    return rows


def create_keyboard(items, rows, cols):
    result = []
    count = 0
    for i in range(0, rows):
        item = []
        for j in range(0, cols):
            try:
                item.append(items[count])
                count += 1
            except BaseException:
                break
        result.append(item)
    return result


def get_reset_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    items = ["/reset"]
    markup.add(*[types.KeyboardButton(name) for name in items])
    return markup


def get_basic_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    items = [u"{} Автобус".format(messages.Emoji.BUS),
             u"{} Троллейбус".format(messages.Emoji.TROLLEYBUS),
             u"{} Трамвай".format(messages.Emoji.TRAM)]
    markup.add(*[types.KeyboardButton(name) for name in items])
    return markup


def get_routes_keyboard(items):
    markup = types.ReplyKeyboardMarkup(row_width=5, one_time_keyboard=True)
    reset = types.KeyboardButton('/reset')
    markup.row(reset)
    markup.add(*[types.KeyboardButton(name) for name in items])
    # reply_keyboard = create_keyboard(items=items, rows=get_dimension(items.__len__(), cols=5), cols=5)
    # markup. append(u"/reset")
    # reset = types.KeyboardButton('/reset')
    markup.row(reset)
    # result = types.ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    return markup


def get_directions_keyboard(items):
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    reset = types.KeyboardButton('/reset')
    markup.row(reset)
    markup.add(*[types.KeyboardButton(name) for name in items])
    # reply_keyboard = create_keyboard(items=items, rows=get_dimension(items.__len__(), cols=5), cols=5)
    # markup. append(u"/reset")
    # reset = types.KeyboardButton('/reset')
    markup.row(reset)
    # result = types.ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    return markup
    # reply_keyboard = create_keyboard(items=items, rows=items.__len__(), cols=1)
    # reply_keyboard.append(u"/reset")
    # result = types.ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # return result


def get_stops_keyboard(items):
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    reset = types.KeyboardButton('/reset')
    markup.row(reset)
    markup.add(*[types.KeyboardButton(name) for name in items])
    # reply_keyboard = create_keyboard(items=items, rows=get_dimension(items.__len__(), cols=5), cols=5)
    # markup. append(u"/reset")
    # reset = types.KeyboardButton('/reset')
    markup.row(reset)
    # result = types.ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    return markup
    # reply_keyboard = create_keyboard(items=items, rows=items.__len__(), cols=1)
    # reply_keyboard.append(u"/reset")
    # result = types.ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # return result