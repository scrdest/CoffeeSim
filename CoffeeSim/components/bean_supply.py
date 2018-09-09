# -*- coding: utf-8 -*-
"""DDD."""

import CoffeeSim.Constants as Constants
const = Constants.Unlocalized

class Container(object):
    
    def __init__(self, contents=None, *args, **kwargs):
        self.contents = set()
        after_fill = self.fill(container=self.contents, fill_contents=contents)
        self.contents.update(after_fill)
        
    def fill(self, fill_contents=None, container=None, *args, **kwargs):
        """Adds specified contents to the target container. 
        
        :param container: optional; a Set-like, holding tank contents
        :param fill_contents: optional; a Mapping of types to volumes
        """
        filled = set()
        filled.update(fill_contents or {})
        return filled