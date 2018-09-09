# -*- coding: utf-8 -*-
"""DDD."""

import copy

import CoffeeSim.Constants as Constants
const = Constants.Unlocalized

from CoffeeSim.helpers import make_sounds


class Tank(object):
    """A generic water tank."""
    capacity = 500
    
    def __init__(self, contents=None, *args, **kwargs):
        self.contents = set()
        after_fill = self.fill(container=self.contents, fill_contents=contents)
        self.contents.update(after_fill)
    
    @staticmethod
    def get_volume(container, *args, **kwargs):
        return sum(( contents.volume for contents in container ))
    
    @property
    def contents_volume(self, *args, **kwargs):
        return self.get_volume(container=self.contents)
        
    def fill(self, fill_contents=None, container=None, *args, **kwargs):
        """Adds specified contents to the target container, respecting tank capacity. 
        
        :param container: optional; a Set-like, holding tank contents
        :param fill_contents: optional; a Mapping of types to volumes
        """
        filled_container = self.contents if container is None else (container or set()).copy()
    
        for cont, vol in (fill_contents or {}).items():
            if vol > (self.capacity - self.get_volume(filled_container)): raise RuntimeWarning("Contents volume exceeds capacity!")
            # in the future, could possibly fill to capacity and discard the rest; sticking to YAGNI for now.
            filled_container.update({cont(volume=vol, **kwargs)})
        
        return filled_container
        
    def remove(self, remove_volume=0, container=None, *args, **kwargs):
        emptied_container = self.contents if container is None else container.copy()
        removed_contents = set()
        to_remove = remove_volume
        
        while to_remove and emptied_container:
            pool_count = len(emptied_container)
            content = emptied_container.pop()
            
            amt_removed = min(content.volume, to_remove / float(pool_count)) # float() for backwards compatibility
            
            removed = copy.deepcopy(content)
            
            make_sounds("GLUG-GLUG-GLUG...")
            content.volume = content.volume - amt_removed
            removed.volume = amt_removed
            
            to_remove -= amt_removed
            
            if content.volume > 0: emptied_container.update([content]) # put the remainder back in
            if removed.volume > 0: removed_contents.update([removed])
        
        else:
            if to_remove: raise RuntimeWarning("Amount to remove ({amt}) exceeded available amount by {rem}."
                                               .format(amt=remove_volume, rem=to_remove)
                                               )
            
        return emptied_container, removed_contents
        
            
    