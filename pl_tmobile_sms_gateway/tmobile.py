# -*- coding: utf-8 -*-

from .base import Base


class Sponsored(Base):

    def base_url(self):
        return "http://www.t-mobile.pl/msg/api/do/tinker/sponsored"


class Omnix(Base):

    def base_url(self):
        return "http://www.t-mobile.pl/msg/api/do/tinker/omnix"
