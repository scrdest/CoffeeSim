# -*- coding: utf-8 -*-
"""Heating elements."""

from Constants import Unlocalized as const

from helpers import make_sounds

class Heater(object):
    def __init__(self, *args, **kwargs):
        pass
        
    def heat(self, items=None, target_temp=None, *args, **kwargs):
        if not items: items = []
        results = {}
        for heated in items:
            heated.temperature = heated.temperature if target_temp is None else target_temp
            # simplistic, but I am *NOT* modelling thermodynamics unless I have to.
            make_sounds("Hissssssss...")
            results[heated] = heated
        return results