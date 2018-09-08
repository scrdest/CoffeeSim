# -*- coding: utf-8 -*-
"""DDD."""

from Constants import Unlocalized as const

from helpers import make_sounds

class Grinder(object):
    def __init__(self, *args, **kwargs):
        pass
        
    def grind(self, items, *args, **kwargs):
        grounded = dict(items)
        grounds = {}
        
        while grounded:
            item, grind_amt = grounded.popitem()
            make_sounds("WHIRRRRRRRR!")
            try: grounds[item] = item.grind(amount=grind_amt, **kwargs)
            # TODO: error handling (I'd rather not add broad exceptions blindly here)
            finally: pass 
        
        return grounds