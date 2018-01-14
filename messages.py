# -*- coding: utf-8 -*-
from enum import Enum


class Emoji(Enum):
    NOT_AVAILABLE = u'🚫'
    NOT_WORKING = u'⚠'
    PREVIOUS = u'◀'
    NEXT = u'▶'
    FUTURE = u'⏩'
    BUS = u'🚌'
    TROLLEYBUS = u'🚎'
    TRAM = u'🚃'
    TUBE = u'🚇'


def get_transport_by_alias(alias):
    if alias == u'{} Автобус'.format(Emoji.BUS):
        return u'autobus'
    elif alias == u'{} Троллейбус'.format(Emoji.TROLLEYBUS):
        return u'trolleybus'
    elif alias == u'{} Трамвай'.format(Emoji.TRAM):
        return u'tram'


def get_icon_by_name(transport):
    if transport == u'autobus':
        return Emoji.BUS
    elif transport == u'trolleybus':
        return Emoji.TROLLEYBUS
    elif transport == u'tram':
        return Emoji.TRAM


def message_ask_for_stop():
    text = u'Выберите остановку:'
    return text


def message_ask_for_direction():
    text = u'Выберите направление:'
    return text


def message_ask_for_route():
    text = u'Выберите маршрут:'
    return text


def message_ask_for_transport():
    text = u'Выберите транспорт:'
    return text


def message_not_available():
    text = u"{} Не удалось получить информацию".format(Emoji.NOT_AVAILABLE)
    return text


def message_not_working():
    text = u'{} Транспорт сегодня не ходит'.format(Emoji.NOT_WORKING)
    return text


def message_schedule_info(transport, route, stop, times):
    text = u'Расписание для\n{transport} {route} {stop}\n{past}: {past_t}  {next}: {next_t}  {future}: {future_t}'.format(
        transport=get_icon_by_name(transport),
        route=route,
        stop=stop,
        past=Emoji.PREVIOUS,
        past_t=times[0],
        next=Emoji.NEXT,
        next_t=times[1],
        future=Emoji.FUTURE,
        future_t=times[2]
    )

