# -*- coding: utf-8 -*-
from .variables import isLinux, isMac


class Icons:
    hasSupport = isLinux or isMac

    # --------------------------------------- #

    EMPTY = '  '
    BOOK = '📒' if hasSupport else ''
    CLOVER = '🍀' if hasSupport else '#'
    LINK = '🔗' if hasSupport else '-'
    HANDS = '🙏' if hasSupport else '-'
    ERROR = '❗' if hasSupport else '!'
    PARTY = '📦' if hasSupport else '$'
    SOUND = '🔊' if hasSupport else '<<'
    SPARKLE = '✨' if hasSupport else '*'
    INFO = '💁  ' if hasSupport else ': '
    RIGHT_ARROW = '➡' if hasSupport else '->'
# end def
