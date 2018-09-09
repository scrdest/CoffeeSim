# -*- coding: utf-8 -*-
"""DDD."""

import CoffeeSim.Constants as Constants
const = Constants.Unlocalized

from CoffeeSim.helpers import make_sounds

class Grinder(object):
    def __init__(self, *args, **kwargs):
        pass
        
    def grind(self, items=None, *args, **kwargs):
        grounded = dict(items or {})
        grounds = {}
        
        while grounded:
            item, grind_amt = grounded.popitem()
            make_sounds("WHIRRRRRRRR!")
            try: grounds[item] = item.grind(amount=grind_amt, **kwargs)
            # TODO: error handling (I'd rather not add broad exceptions blindly here)
            finally: pass 
        
        return grounds