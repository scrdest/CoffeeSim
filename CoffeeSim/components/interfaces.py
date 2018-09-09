# -*- coding: utf-8 -*-
"""Physical interface elements - buttons, LEDs, etc."""

import weakref

import CoffeeSim.Constants as Constants
const = Constants.Unlocalized

def _placeholder_func(*args, **kwargs): return

class Button(object):
    """A (physical) button. May trigger various functionalities upon being pressed."""
    default_onPress = None
    
    def __init__(self, owner=None, onPress=None, *args, **kwargs):
        self.onPress = onPress if onPress else self.default_onPress or _placeholder_func
        if not hasattr(self.onPress, '__call__'): raise TypeError('onPress should be a callable!')
        
        self.owner = weakref.ref(owner)
        
    def press(self, *args, **kwargs):
        """Responds to the button being pressed. Exact semantics depend on the button setup."""
        return self.onPress(*args, **kwargs)
        
        
class PowerButton(Button):
    """A power toggle button."""
    def toggle_power(self, *args, **kwargs):
        owner = self.owner()
        if owner: owner.powered = not owner.powered
        
    default_onPress = toggle_power
        
        
class CoffeeButton(Button):
    def __init__(self, owner=None, onPress=None, preset=None, *args, **kwargs):
        super(CoffeeButton, self).__init__(owner=owner, onPress=onPress, *args, **kwargs)
        self.preset = preset

    def send_preset(self, *args, **kwargs):
        owner = self.owner()
        if owner: owner.brew(preset=self.preset)
        
    default_onPress = send_preset
    
    