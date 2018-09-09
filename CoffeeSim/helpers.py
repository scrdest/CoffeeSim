# -*- coding: utf-8 -*-
"""Assorted utility functions that might be needed throughout the project and should be shared."""

import CoffeeSim.Constants as Constants

def make_sounds(sound, *sounds, **kwargs):
    """Helper; just to avoid reliance on bare print()s for I/O."""
    if Constants.USE_SOUND_EFFECTS: print(str(sound) + ", ".join(map(str, sounds)))