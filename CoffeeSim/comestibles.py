# -*- coding: utf-8 -*-
"""Holds definitions of unprocessed materials and the delicious brews made with them."""

import CoffeeSim.Constants as Constants
const = Constants.Unlocalized

class CaffeineSource(object):
    extract_efficiency = 10
    
    def __init__(self, amount=1, caffeine_density=1, *args, **kwargs):
        if amount < 0: raise ValueError(
            "Amount should be a positive value! Value received: {val}.".format(val=amount)
        )
        if caffeine_density < 0: caffeine_density = 0 # clip to a more sensible value
        self.amount = amount
        self.caffeine_density = caffeine_density
        
    def extract(self, extract_efficiency=NotImplemented, *args, **kwargs):
        """Handles caffeine extraction.
        
        :param extract_efficiency: optional override; how much of the total caffeine is extracted.
        """
        extract_efficiency = self.extract_efficiency if extract_efficiency is NotImplemented else extract_efficiency
        
        curr_caffeine = self.amount * self.caffeine_density
        extracted_caffeine = curr_caffeine * 0.01 * extract_efficiency
        curr_caffeine -= extracted_caffeine
        
        self.caffeine_density = curr_caffeine / self.amount
        
        return extracted_caffeine
        
    def __str__(self): return ("{name} (Amount: {amt}) <Caffeine: {caf} units>"
                                .format(
                                        name=type(self).__name__, 
                                        amt=self.amount,
                                        caf=self.caffeine_density * self.amount,
                                        ))
    
    
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
    """Like coffee beans, except ground. 
    
    The increased contact surface enables more caffeine to be extracted.
    """
    extract_efficiency = 90
    
        
class Liquid(object):
    display_name = const.LOC_LIQUID

    freezing_point = const.WATER_FREEZE_PT
    evaporation_point = const.WATER_EVAPORATE_PT
    
    @property
    def description(self): return ("{} ".format(" ".join(map(str, sorted(self.descriptors))))) if self.descriptors else ""
    
    def __init__(self, volume=Constants.DEFAULT_VOLUME, temperature=const.ROOMTEMP, *args, **kwargs):
        if volume <= 0: raise ValueError(
            "Liquids must have a positive, nonzero volume! Value received: {val}.".format(val=volume)
        )
        
        if temperature < const.ABS_ZERO: raise ValueError(
            "Temperature must exceed 0K! Value received: {val} {unit}.".format(val=volume, unit=const.TEMP_UNIT)
        )
        
        if temperature > self.evaporation_point or temperature < self.freezing_point: raise RuntimeWarning(
            "The material would not be liquid at the provided temperature. Value received: {val} {unit}.".format(val=temperature, unit=const.TEMP_UNIT)
        )
        
        self.volume = volume
        self.temperature = temperature
        
        self.descriptors = set()
        
    def update_state(self):
        descriptors = set()
        
        warmth = self.temperature
        warmth_desc = const.WARMTH_FROZEN
        temp_thresholds = [
                    (self.freezing_point, const.WARMTH_ICY), 
                    (((const.ROOMTEMP - self.freezing_point) / 2), const.WARMTH_COLD), 
                    ((const.ROOMTEMP - 5), const.WARMTH_MED), 
                    ((const.ROOMTEMP + 15), const.WARMTH_WARM), 
                    (((self.evaporation_point - const.ROOMTEMP) / 2), const.WARMTH_HOT), 
                    (self.evaporation_point, const.WARMTH_BOILING)
                    ]
        
        for threshold in temp_thresholds:
            if self.temperature > threshold[0]: warmth_desc = threshold[1]
            
        descriptors |= {warmth_desc}
        
        self.descriptors = descriptors # only update the whole description all at once, to ensure data integrity
        return descriptors
    
    def __str__(self): 
        self.update_state()
        return "{desc}{name} ({volume}{unit})".format(
                                                    desc=(", ".join(sorted(self.descriptors)) + (" " if self.descriptors else "")), 
                                                    name=self.display_name, 
                                                    volume=self.volume, 
                                                    unit=const.VOLUME_UNIT,
                                            )
    
class Water(Liquid):
    display_name = const.LOC_WATER
    
class Coffee(Liquid):
    display_name = const.LOC_COFFEE
    
    def __init__(self, 
                 volume=Constants.DEFAULT_VOLUME, 
                 temperature=const.ROOMTEMP, 
                 caffeine_content=0, 
                 name_override=NotImplemented, 
                 extras=None,
                 *args, **kwargs):
                
        super(Coffee, self).__init__(volume=volume, temperature=temperature, *args, **kwargs)
        self.caffeine_content = max(0, caffeine_content)
        if name_override is not NotImplemented: self.display_name = name_override
        self.extras = extras or []
        
    def update_state(self):
        descriptors = super(Coffee, self).update_state()
        
        strength = self.caffeine_content
        strength_desc = const.STRENGTH_DECAF
        
        strength_thresholds = [
                              (5, const.STRENGTH_LOW), 
                              (50, const.STRENGTH_MEDIUM), 
                              (150, const.STRENGTH_HIGH),
                              ]
        
        for threshold in strength_thresholds:
            if strength > threshold[0]: strength_desc = threshold[1]
        
        descriptors |= {strength_desc}
        
    def __str__(self):
        base_representation = super(Coffee, self).__str__()
        extras_desc = []
        if self.extras: extras_desc = [str(extra) for extra in self.extras]
        
        extras_desc = " with {}".format(", ".join(extras_desc)) if extras_desc else ""
        
        return base_representation + extras_desc
        
    