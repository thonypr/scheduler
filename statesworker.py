# -*- coding: utf-8 -*-
import json
import jsonpath
import mmap


# Пытаемся узнать из базы «состояние» пользователя
def get_current_state(user_id):
    try:
        f = open('{}.txt'.format(user_id))
        state = f.readline()
        f.close()
        return state
    except IOError:
    # create the  and set start value
        f = open("{}.txt".format(user_id), "w")
        f.write("0")
        f.close()
        return 0


# Сохраняем текущее «состояние» пользователя в нашу базу
def set_state(user_id, value):
    # with Vedis(config.db_file) as db:
    #     try:
    #         db[user_id] = value
    #         return True
    #     except:
    #         тут желательно как-то обработать ситуацию
            # return False
    try:
        f = open('{}.txt'.format(user_id), "w")
        f.write("{}".format(value))
        state = f.readline()
        f.close()
        return True
    except :
    # create the  and set start value

        return False


get_current_state(57438934)
set_state(57438934, 2)
i = 0