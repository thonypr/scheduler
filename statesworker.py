# -*- coding: utf-8 -*-


# Пытаемся узнать из базы «состояние» пользователя
def get_current_state(user_id, history):
    if history.get(user_id) is not None:
        return history[user_id].state
    else:
        return u'0'
