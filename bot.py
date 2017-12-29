# -*- coding: utf-8 -*-
import os
import telebot
import minsk_trans
from telebot import types
# import requests
import json

# token = os.environ['TELEGRAM_TOKEN']
token = u"424882927:AAGKLtBw6ZmZyQQH9mfSKVpztQO6LxzyNX8"
# If you use redis, install this add-on https://elements.heroku.com/addons/heroku-redis
# r = redis.from_url(os.environ.get("REDIS_URL"))

#       Your bot code below
bot = telebot.TeleBot(token)
init = None
transport = None
# route_name = None
route_number = None
stop = None
time = None


@bot.message_handler(content_types=[u"text"])
def handle_start(message):
    global init
    global transport
    # global route_name
    global route_number
    global stop
    global time
    to = message.from_user.id
    if not init:
        transport_keys = types.ReplyKeyboardMarkup(row_width=3)
        itembtn1 = types.KeyboardButton('autobus')
        itembtn2 = types.KeyboardButton('trolleybus')
        itembtn3 = types.KeyboardButton('tram')
        transport_keys.add(itembtn1, itembtn2, itembtn3)
        bot.send_message(to, "Select transport:", reply_markup=transport_keys)
        init = 1
    elif not transport:
        transport = message.text
        numbers = minsk_trans.get_routes_html(transport)
        numbers_count = numbers.__len__()
        route_numbers_keys = types.ReplyKeyboardMarkup(row_width = numbers_count)
        for route in numbers:
            button = types.KeyboardButton(u'{}'.format(route))
            route_numbers_keys.add(button)
        bot.send_message(to, "Select route number:", reply_markup=route_numbers_keys)
    elif not stop:
        route_number = message.text
        route_name, original_stops, reversed_name, reversed_stops = minsk_trans.get_stops_by_transport_and_number(transport, route_number)
        keys_count = original_stops.__len__() + reversed_stops.__len__() + 2
        stops_keys = types.ReplyKeyboardMarkup(row_width=keys_count)
        stops_keys.add(u'{}'.format(route_name))
        for stop in original_stops:
            button = types.KeyboardButton(u'{}'.format(stop))
            stops_keys.add(button)
        stops_keys.add(u'{}'.format(reversed_name))
        for stop in reversed_stops:
            button = types.KeyboardButton(u'{}'.format(stop))
            stops_keys.add(button)
        bot.send_message(to, u"Select direction and stop:", reply_markup=stops_keys)
    elif not time:
        stop = message.text
        route_name, original_stops, reversed_name, reversed_stops = minsk_trans.get_stops_by_transport_and_number(
            transport, route_number)
        #TODO: works only with > directions. Divide it to selecting route(direction)
        times = minsk_trans.get_around_times_at_stop(transport, route_number, route_name, stop)
        bot.send_message(to, u"Passed was at: {0}\nNext will be at: {1}\nFuture will be at: {2}".format(times[0], times[1], times[2]))
        init = None
        transport = None
        # route_name = None
        route_number = None
        stop = None
        time = None
    # bot.send_message(to, u"test")

    # text = u'{}'.format(message.text)
    # amount = text.split(u' ')[0]
    # if type(amount) is float or int:
    #     try:
    #         print (text.split(u' ').__len__())
    #         if text.split(u' ').__len__() == 2:
    #             if has_dollar_names(text):
    #                 byn = get_byn_amount(amount=amount, currency=u"USD")
    #                 eur_rate = get_byn_amount(amount=1, currency=u"EUR")
    #                 eur_amount = round(byn / eur_rate, 2)
    #                 bot.send_message(to, u"🇺🇸 {0}\n🇧🇾{1}\n🇪🇺{2}".format(amount, byn, eur_amount))
    #                 print (u"Message to{0}:\n🇺🇸 {1}\n🇧🇾{2}\n🇪🇺{3}".format(to, amount, byn, eur_amount))
    #             elif has_euro_names(text):
    #                 byn = get_byn_amount(amount=amount, currency=u"EUR")
    #                 usd_rate = get_byn_amount(amount=1, currency=u"USD")
    #                 usd_amount = round(byn / usd_rate, 2)
    #                 bot.send_message(to, u"🇺🇸 {0}\n🇧🇾{1}\n🇪🇺{2}".format(usd_amount, byn, amount))
    #                 print (u"Message to{0}:\n🇺🇸 {1}\n🇧🇾{2}\n🇪🇺{3}".format(to, usd_amount, byn, amount))
    #             else:
    #                 usd_rate = get_byn_amount(amount=1, currency=u"USD")
    #                 usd_amount = round(int(amount) / usd_rate, 2)
    #                 eur_rate = get_byn_amount(amount=1, currency=u"EUR")
    #                 eur_amount = round(int(amount) / eur_rate, 2)
    #                 bot.send_message(to, u"🇺🇸 {0}\n🇧🇾{1}\n🇪🇺{2}".format(usd_amount, amount, eur_amount))
    #                 print (u"Message to{0}:\n🇺🇸 {1}\n🇧🇾{2}\n🇪🇺{3}".format(to, usd_amount, amount, eur_amount))
    #         else:
    #             bot.send_message(to, u"Неверный ввод. Введите в формате Число Валюта")
    #             print (u"Message to{0}:\nНеверный ввод. Введите в формате Число Валюта".format(to))
    #     except ValueError:
    #         bot.send_message(to, u"Неверный ввод. Введите в формате Число Валюта")
    #         print (u"Message to{0}:\nНеверный ввод. Введите в формате Число Валюта".format(to))
    # else:
    #     bot.send_message(to, u"Неверный ввод. Введите в формате Число Валюта")
    #     print (u"Message to{0}:\nНеверный ввод. Введите в формате Число Валюта".format(to))


# def get_byn_amount(currency, amount):
#     url = "http://www.nbrb.by/API/ExRates/Rates/{}".format(currency)
#
#     querystring = {"ParamMode": "2"}
#
#     try:
#         response = requests.request("GET", url, params=querystring)
#         r = json.loads(response.content)
#         return round(float(r['Cur_OfficialRate']) * float(amount), 2)
#     except BaseException:
#         return u"Что-то пошло не так..."
#
#
# def has_dollar_names(message):
#     synonyms = [u'доллар', u'бакс', u'dollar', u'$', u'бакинских']
#     for synonym in synonyms:
#         if message.lower().__contains__(synonym):
#             return True
#     return False
#
#
# def has_euro_names(message):
#     synonyms = [u'евро', u'еврик', u'euro', u'€']
#     for synonym in synonyms:
#         if message.lower().__contains__(synonym):
#             return True
#     return False


bot.polling(none_stop=True, interval=0)