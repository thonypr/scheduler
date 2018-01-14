# -*- coding: utf-8 -*-

import telebot
import config
import os
import statesworker
import history
import keyboards
import minsk_trans
import messages

token = os.environ['TELEGRAM_TOKEN']
# token = config.token

bot = telebot.TeleBot(token)
history_items = {}


# Начало диалога
@bot.message_handler(commands=["start"])
def cmd_start(message):
    history_item = history.History(user=message.chat.id, state=config.States.S_ENTER_TRANSPORT)
    if history_items.get(message.chat.id) is None:
        history_items[history_item.user_id] = history_item
    else:
        del history_items[message.chat.id]

    bot.send_message(message.chat.id, messages.message_ask_for_transport(),
                     reply_markup=keyboards.get_basic_keyboard())


# По команде /reset будем сбрасывать состояния, возвращаясь к началу диалога
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    history_item = history.History(user=message.chat.id, state=config.States.S_ENTER_TRANSPORT)
    if history_items.get(message.chat.id) is None:
        history_items[history_item.user_id] = history_item
    else:
        del history_items[message.chat.id]

    bot.send_message(message.chat.id, messages.message_ask_for_transport(),
                     reply_markup=keyboards.get_basic_keyboard())


@bot.message_handler(func=lambda message: statesworker.get_current_state(message.chat.id, history_items) == config.States.S_ENTER_TRANSPORT)
def user_entered_transport(message):
    if history_items.get(message.chat.id) is not None:
        history_items[message.chat.id].transport = messages.get_transport_by_alias(message.text)
        history_items[message.chat.id].state = config.States.S_ENTER_ROUTE
    # Полагаем, что пользователь вводит исходя из кнопок
    routes = minsk_trans.get_routes_html(history_items[message.chat.id].transport)
    try:
        print u"User {user} selected transport:{transport}".format(
        user=message.chat.id,
        transport=history_items[message.chat.id].transport)
    except UnicodeEncodeError:
        print u'User: {user}::Error in print'.format(user=message.chat.id)
    bot.send_message(message.chat.id, messages.message_ask_for_route(),
                     reply_markup=keyboards.get_routes_keyboard(routes))


@bot.message_handler(func=lambda message: statesworker.get_current_state(message.chat.id, history_items) == config.States.S_ENTER_ROUTE)
def user_entered_route(message):
    if history_items.get(message.chat.id) is not None:
        history_items[message.chat.id].route = message.text
        history_items[message.chat.id].state = config.States.S_ENTER_DIRECTION
    # Полагаем, что пользователь вводит исходя из кнопок
    user = message.chat.id
    transport = history_items[user].transport
    route = history_items[user].route
    directions = minsk_trans.get_directions_in_route(transport, route)
    try:
        print u"User {user} selected route:{route}".format(user=message.chat.id, route=message.text)
    except UnicodeEncodeError:
        print u'User: {user}::Error in print'.format(user=message.chat.id)
    bot.send_message(message.chat.id, messages.message_ask_for_direction(),
                     reply_markup=keyboards.get_directions_keyboard(directions))


@bot.message_handler(func=lambda message: statesworker.get_current_state(message.chat.id, history_items) == config.States.S_ENTER_DIRECTION)
def user_entered_direction(message):
    if history_items.get(message.chat.id) is not None:
        history_items[message.chat.id].direction = message.text
        history_items[message.chat.id].state = config.States.S_ENTER_STOP
    # Полагаем, что пользователь вводит исходя из кнопок
    user = message.chat.id
    transport = history_items[user].transport
    route = history_items[user].route
    direction = history_items[user].direction
    stops = minsk_trans.get_stops_in_route(transport, route, direction)
    try:
        print u"User {user} selected direction:{direction}".format(user=message.chat.id, direction=message.text)
    except UnicodeEncodeError:
        print u'User: {user}::Error in print'.format(user=message.chat.id)
    bot.send_message(message.chat.id, messages.message_ask_for_stop(),
                     reply_markup=keyboards.get_stops_keyboard(stops))


@bot.message_handler(func=lambda message: statesworker.get_current_state(message.chat.id, history_items) == config.States.S_ENTER_STOP)
def user_entered_stop(message):
    if history_items.get(message.chat.id) is not None:
        history_items[message.chat.id].stop = message.text
        history_items[message.chat.id].state = config.States.S_START
    item = history_items[message.chat.id]
    # Полагаем, что пользователь вводит исходя из кнопок
    user = message.chat.id
    transport = history_items[user].transport
    route = history_items[user].route
    direction = history_items[user].direction
    stop = history_items[user].stop
    times = minsk_trans.get_around_times_at_stop(transport, route, direction, stop)
    try:
        print u"User {user} selected stop:{stop}".format(user=message.chat.id, stop=message.text)
    except UnicodeEncodeError:
        print u'User: {user}::Error in print'.format(user=message.chat.id)
    if times.__len__() < 3:
        bot.send_message(chat_id=message.chat.id, text=messages.message_not_available(),
                         reply_markup=keyboards.get_reset_keyboard())
    elif times[0] == u'E':
        bot.send_message(chat_id=message.chat.id, text=messages.message_not_working(),
                         reply_markup=keyboards.get_reset_keyboard())
    else:
        bot.send_message(chat_id=message.chat.id, text=messages.message_schedule_info(transport, route, stop, times),
                         reply_markup=keyboards.get_reset_keyboard())
    # Добавить запись в файл с ситорией запросов по этому пользователю
    # Из словарика удалить
    # print history_items.items()
    del history_items[message.chat.id]

bot.polling(none_stop=True, interval=0)