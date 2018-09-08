# -*- coding: utf-8 -*-
"""Holds definitions of unprocessed materials and the delicious brews made with them."""

from Constants import Unlocalized as const

class CaffeineSource(object):
    def __init__(self, amount=1, caffeine_density=1, *args, **kwargs):
        if amount < 0: raise ValueError(
            "Amount should be a positive value! Value received: {val}.".format(val=amount)
        )
        if caffeine_density < 0: caffeine_density = 0 # clip to a more sensible value
        self.amount = amount
        self.caffeine_density = caffeine_density
        
    def extract(self, extract_efficiency=99, *args, **kwargs):
        """Handles caffeine extraction.
        
        :param extract_efficiency: optional; how much of the total caffeine is extracted.
        """
        curr_caffeine = self.amount * self.caffeine_density
        extracted_caffeine = curr_caffeine * 0.01 * extract_efficiency
        curr_caffeine -= extracted_caffeine
        self.caffeine_density = curr_caffeine / self.amount
        return extracted_caffeine
    
    
class CoffeeBeans(CaffeineSource):
    """Like coffee grounds, except whole. Also, can be ground."""
    
    def grind(self, amount=0, *args, **kwargs):
        """Handles grinding a specified amount of beans into grounds.
        
        :param amount: amount of beans to grind. 
            If not specified, won't grind any. 
            If provided value is greater than the available amount, grinds down all available beans.
            
        :returns: a dict of objects existing after grinding the beans (i.e. remaining beans and/or created grounds) under string constant keys
        """
        available_amt = self.amount
        ground_amt = min(amount, available_amt)
        
        grounds = CoffeeGrounds(amount=ground_amt, caffeine_density=self.caffeine_density) if ground_amt else None
        
        after_ground = {}
        
        if grounds: after_ground[const.MAT_GROUNDS] = grounds
        
        remainder = available_amt - ground_amt
        if ground_amt < available_amt: after_ground[const.MAT_BEANS] = self
        
        self.amount = remainder
        return after_ground
        
        
class CoffeeGrounds(CoffeeBeans):
    """Like coffee beans, except ground."""
    pass
    
        
class Liquid(object):
    display_name = "Liquid"

    freezing_point = const.WATER_FREEZE_PT
    evaporation_point = const.WATER_EVAPORATE_PT
    
    @property
    def description(self): return ("{} ".format(" ".join(map(str, sorted(self.descriptors))))) if self.descriptors else ""
    
    def __init__(self, volume=const.DEFAULT_VOLUME, temperature=const.ROOMTEMP, *args, **kwargs):
        if volume <= 0: raise ValueError(
            "Liquids must have a positive, nonzero volume! Value received: {val}.".format(val=volume)
        )
        
        if temperature < const.ABS_ZERO: raise ValueError(
            "Temperature must exceed 0K! Value received: {val} {unit}.".format(val=volume, unit=const.TEMP_UNIT)
        )
        
        if temperature > self.evaporation_point or temperature < self.freezing_point: raise RuntimeWarning(
            "Warning: the material would not be liquid at the provided temperature. Value received: {val}.".format(val=volume)
        )
        
        self.volume = volume
        self.temperature = temperature
        
        self.descriptors = set()
        
    def update_state(self):
        descriptors = set()
        
        warmth = self.temperature
        warmth_desc = const.WARMTH_WARM if self.temperature >= const.ROOMTEMP else const.WARMTH_COLD # stub!
        descriptors |= [warmth_desc]
        
        self.descriptors = descriptors # only update the whole description all at once, to ensure data integrity
        return descriptors
    
    def __str__(self): 
        self.update_state()
        return "{desc}{name} ({volume}{unit})".format(
                                                    desc=self.descriptors, 
                                                    name=self.display_name, 
                                                    volume=self.volume, 
                                                    unit='mL'
                                            )
    
class Water(Liquid):
    display_name = "Water"
    
class Coffee(Liquid):
    display_name = "Coffee"
    
    def __init__(self, volume=const.DEFAULT_VOLUME, temperature=const.ROOMTEMP, caffeine_content=0, *args, **kwargs):
        super(Coffee, self).__init__(self, volume=volume, temperature=temperature, *args, **kwargs)
        self.caffeine_content = max(0, caffeine_content)
        
    def update_state(self):
        descriptors = super(Coffee, self).update_state()
        
        strength = self.caffeine_content
        strength_desc = const.STRENGTH_DECAF if self.caffeine_content <= 5 else const.STRENGTH_MEDIUM # stub!
        
        descriptors |= strength_desc
        
        self.descriptors = descriptors
        return descriptors
        
    