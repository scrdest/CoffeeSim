"""Holds the ABC for coffeemaker model definitions.
"""

from Constants import Unlocalized as const

from components import water_supply, bean_supply, grinders, heaters

import comestibles

class AbstractCoffeemaker(object):
    """An abstract base for all Coffeemakers; as such, it only defines the API and is *NOT* suitable for direct use.
    If you need a non-specific *functional* model, see the GenericCoffeemaker subclass.
    """
    # Component 'slots' define what parts the model supports:
    component_slots = {
        const.COMP_WATER : 1,
        const.COMP_BEANS : 1,
        const.COMP_GRINDER : 1,
        const.COMP_HEATER : 1,
        const.COMP_FILTER : 1,
        const.COMP_GROUNDSBIN: 1,
    }
    
    installed_components = {comptype: None for comptype in component_slots}
    
    def __init__(self, *args, **kwargs): raise NotImplementedError

    def brew(self, coffee_volume=const.DEFAULT_VOLUME, strength=const.STRENGTH_MEDIUM, *args, **kwargs):
        """High-level brewing simulation.
        
        :param coffee_volume: optional, numeric; how much coffee to brew.
        :param strength: optional, string constant; how strong the brew should be.
        :param **kwargs: passed along to callees.
        """
        water = self.get_water(volume=coffee_volume, **kwargs)
        grounds = self.get_grounds(strength=strength, **kwargs)
        
        extract = self.extract_coffee(grounds=grounds, medium=water, **kwargs)
        
        self.grounds_dispose(grounds, **kwargs)
        
        coffee = self.handle_extras(extract=extract, **kwargs)
        
        return coffee
        
    def get_water(self, volume=const.DEFAULT_VOLUME, *args, **kwargs):
        """Handles the provision of water for the extraction process.
        
        :param volume: optional, numeric; requested amount of water.
        :param **kwargs: passed to callees.
        """
        sources = self.installed_components.get(const.COMP_WATER)
        if not sources: raise RuntimeError("No water sources available!")
        sources = {src: src.contents_volume for src in sources}
        
        obtained_vol, needed_vol = 0, volume
        
        available_vol = sum(( contents for contents in sources.values() ))
        if available_vol < needed_vol: raise RuntimeError("Water levels insufficient!")
        
        while obtained_vol < needed_vol:
            water_sources = self.pick_water_sources(sources=sources, needed_amt=needed_vol, **kwargs)
            print(water_sources)
            for (curr_src, curr_vol) in water_sources.items():
                curr_src.contents, obtained_vol = ( curr_src.remove(remove_volume=curr_vol) ), (obtained_vol + curr_vol) 
                # a bit ugly to use tuple unpacking here, but it should enforce the synchronization of transfer on both ends.
                if obtained_vol >= needed_vol: break # shouldn't really be necessary, but there's no harm in being a bit paranoid.
        
    def pick_water_sources(self, sources, needed_amt, *args, **kwargs):
        """Handles selecting how much water to retrieve and from which source.
        
        :param sources: water sources to choose from; Mapping of objects to stored volumes.
        :param needed_amt: numeric; the requested volume of water.
        :returns: a dict of sources used and the volume of water to obtain from each source.
        """
        remaining_amt = needed_amt
        solution = {}
        # very simple algorithm: greedily exhaust each source in the order of traversal
        # could be overridden in a subclass for a smarter protocol, e.g. try to empty out the tanks first.
        for src, vol in sources.items():
            used_vol = min(vol, remaining_amt)
            remaining_amt -= used_vol
            solution[src] = used_vol        
        return solution
    
    def get_grounds(self, *args, **kwargs):
        """Handles the provision of coffee grounds for the extraction process. """
        raise NotImplementedError
        
    def extract(grounds=None, water=None, *args, **kwargs):
        if not grounds and water: return water
        
        caffeine = grounds.extract()
        brew = comestibles.Coffee(
                                  volume=water.volume, 
                                  temperature=0.8*(const.WATER_EVAPORATE_PT-const.WATER_FREEZE_PT), 
                                  caffeine_content=caffeine,
                                  )
        
    
class GenericCoffeemaker(AbstractCoffeemaker):
    """An example using a non-specific, off-brand, made-up coffeemaker model 
    to demo the simulation functionality.
    """
    
    def __init__(self, *args, **kwargs): 
        self.installed_components = {
            const.COMP_WATER : [water_supply.Tank(contents={comestibles.Water: water_supply.Tank.capacity})],
            const.COMP_BEANS : [bean_supply.Container()],
            const.COMP_GRINDER : [grinders.Grinder()],
            const.COMP_HEATER : [heaters.Heater()],
            # const.COMP_FILTER : [],
            # const.COMP_GROUNDSBIN: [],
        }
    
    def get_grounds(self, *args, **kwargs):
        sources = self.installed_components.get(const.COMP_BEANS)
        grinders = self.installed_components.get(const.COMP_GRINDER)
        if not sources: raise RuntimeError("Coffee bin not found!")
        if not grinders: raise RuntimeError("No operational bean grinder found!")
        beans = comestibles.CoffeeBeans(amount=100)
        grounds = beans.grind(amount=100) # TODO move this operation into the grinder's grind method
        return grounds
        
    
Coffeemaker = GenericCoffeemaker # alias
