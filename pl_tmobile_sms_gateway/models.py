# -*- coding: utf-8 -*-


class GatewayResponse:
    def __init__(self, ok, message, tokens_left=None):
        self.ok = ok
        self.message = message
        self.tokens_left = tokens_left
