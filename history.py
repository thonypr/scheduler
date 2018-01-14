# -*- coding: utf-8 -*-


class History:
    def __init__(self,
                 state,
                 user,
                 transport=None,
                 route=None,
                 direction=None,
                 stop=None):
        self.user_id = user
        self.transport = transport
        self.route = route
        self.direction = direction
        self.stop = stop
        self.state = state

    # user_id, transport, route, direction, stop



