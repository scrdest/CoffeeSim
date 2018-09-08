# -*- coding: utf-8 -*-
"""Assorted utility functions that might be needed throughout the project and should be shared."""

def make_sounds(sound, *sounds, **kwargs):
    """Helper; just to avoid reliance on bare print()s for I/O."""
    print(sound, *sounds)