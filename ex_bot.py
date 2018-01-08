#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import math
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import minsk_trans
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)
TRANSPORT, ROUTE, DIRECTION, STOP = range(4)
answers = []


# def start(bot, update):
#     reply_keyboard = [['Boy', 'Girl', 'Other']]
#
#     update.message.reply_text(
#         'Hi! My name is Professor Bot. I will hold a conversation with you. '
#         'Send /cancel to stop talking to me.\n\n'
#         'Are you a boy or a girl?',
#         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
#
#     return

def start(bot, update):
    reply_keyboard = [['autobus', 'trolleybus', 'tram']]
    answer = {}
    answer["user_id"] = update.message.from_user.id
    answers.append(answer)

    update.message.reply_text(
        'Выберите вид транспорта',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return GENDER

# def gender(bot, update):
#     user = update.message.from_user
#     logger.info("Gender of %s: %s", user.first_name, update.message.text)
#     update.message.reply_text('I see! Please send me a photo of yourself, '
#                               'so I know what you look like, or send /skip if you don\'t want to.',
#                               reply_markup=ReplyKeyboardRemove())
#
#     return PHOTO


def get_dimension(count, cols):
    # side = math.sqrt(count)
    # whole = math.trunc(side)
    # return whole + 1
    rows = int(math.trunc(count/cols))+1
    return rows


def create_keyboard(routes, rows, cols):
    result = []
    count = 0
    for i in range(0, rows):
        item = []
        for j in range(0, cols):
            try:
                item.append(routes[count])
                count = count + 1
            except BaseException:
                break
        result.append(item)
    return result


def get_answer_from_history(answers, user):
    for answer in answers:
        if answer["user_id"] == user:
            return answer
    return None


def gender(bot, update):
    answer = get_answer_from_history(answers, update.message.from_user.id)
    if answer is None:
        answer = {}
        answers.append(answer)
        answer = answers.pop()
    answer["transport"] = update.message.text
    routes = minsk_trans.get_routes_html(answer["transport"])
    # reply_keyboard = ReplyKeyboardMarkup(routes)
    # i = 0
    # for route in routes:
    #     if
    # reply_keyboard = [routes]
    reply_keyboard = create_keyboard(routes=routes, rows=get_dimension(routes.__len__(), cols=5), cols=5)
    # reply_keyboard = [['1','2','3'],
    #                   ['4','5','6'],
    #                   ['7','8','9']]

    # for route in routes:
    #     button = KeyboardButton(u'{}'.format(route))
    #     reply_keyboard.add(button)

    user = update.message.from_user
    logger.info("Transport for %s: %s", user.first_name, answer["transport"])
    update.message.reply_text('I see! Choose route number',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))

    return PHOTO


# def photo(bot, update):
#     user = update.message.from_user
#     photo_file = bot.get_file(update.message.photo[-1].file_id)
#     photo_file.download('user_photo.jpg')
#     logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
#     update.message.reply_text('Gorgeous! Now, send me your location please, '
#                               'or send /skip if you don\'t want to.')
#
#     return LOCATION

def photo(bot, update):

    user = update.message.from_user
    answer = get_answer_from_history(answers, user.id)
    route_number = update.message.text
    answer["route_number"] = route_number
    directions = minsk_trans.get_directions_in_route(answer["transport"], answer["route_number"])
    # photo_file = bot.get_file(update.message.photo[-1].file_id)
    # photo_file.download('user_photo.jpg'
    reply_keyboard = create_keyboard(routes=directions, rows=directions.__len__(), cols=1)
    logger.info("Route number of %s: %s", user.first_name, answer["route_number"])
    update.message.reply_text('Gorgeous! Now, send me route direction',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return LOCATION


def skip_photo(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your location please, '
                              'or send /skip.')

    return LOCATION


def location(bot, update):
    user = update.message.from_user
    answer = get_answer_from_history(answers, user.id)
    answer["direction"] = update.message.text
    stops = minsk_trans.get_stops_by_transport_and_number(answer["transport"], answer["route_number"])
    reply_keyboard = create_keyboard(routes=stops, rows=stops.__len__(), cols=5)
    # user_location = update.message.location
    logger.info("Stop for of %s: %s", user.first_name, answer["direction"])
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return BIO


def skip_location(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return BIO


def bio(bot, update):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("424882927:AAGKLtBw6ZmZyQQH9mfSKVpztQO6LxzyNX8")
    # updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            GENDER: [RegexHandler('^(autobus|trolleybus|tram)$', gender)],

            PHOTO: [MessageHandler(Filters.text, photo),
                    CommandHandler('skip', skip_photo)],

            LOCATION: [MessageHandler(Filters.text, location),
                       CommandHandler('skip', skip_location)],

            BIO: [MessageHandler(Filters.text, bio)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()