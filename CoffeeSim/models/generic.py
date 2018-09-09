"""Holds the ABC for coffeemaker model definitions.
"""

import CoffeeSim.Constants as Constants
const = Constants.Unlocalized

from CoffeeSim.components import water_supply, bean_supply, grinders, heaters, interfaces

import CoffeeSim.comestibles as comestibles

from CoffeeSim.helpers import make_sounds

class AbstractCoffeemaker(object):
    """An abstract base for all Coffeemakers; as such, it only defines the API and is *NOT* suitable for direct use.
    If you need a non-specific *functional* model, see the GenericCoffeemaker subclass.
    """
    powered = False
    
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

    def brew(self, preset=None, coffee_volume=None, *args, **kwargs):
        """High-level brewing simulation.
        
        :param preset: optional; a drink type preset to use, e.g. Espresso or Americano.
        :param coffee_volume: optional, numeric; how much coffee to brew. If specified, overrides the preset value.
        :param **kwargs: passed along to callees.
        """
        if not self.powered: return None
        coffee_volume = coffee_volume or (preset.volume if preset else None) or Constants.DEFAULT_VOLUME
        strength = preset.strength if preset else const.STRENGTH_MEDIUM
        
        water = self.get_water(volume=coffee_volume, **kwargs)
        grounds = self.get_grounds(strength=strength, **kwargs)
        
        extract, spent_grounds = self.get_extract(grounds=grounds, medium=water, **kwargs)
        
        self.grounds_dispose(grounds=spent_grounds, **kwargs)
        
        coffee = self.get_extras(brew=extract, **kwargs)
        
        return coffee
        
    def get_water(self, volume=Constants.DEFAULT_VOLUME, *args, **kwargs):
        """Handles the provision of water for the extraction process.
        
        :param volume: optional, numeric; requested amount of water.
        :param **kwargs: passed to callees.
        """
        if not self.powered: return None
        
        sources = self.installed_components.get(const.COMP_WATER)
        if not sources: raise RuntimeError("No water sources available!")
        sources = {src: src.contents_volume for src in sources}
        
        water_found = set()
        obtained_vol, needed_vol = 0, volume
        
        available_vol = sum(( contents for contents in sources.values() ))
        if available_vol < needed_vol: raise RuntimeError("Water levels insufficient!")
        
        while obtained_vol < needed_vol:
            water_sources = self.pick_water_sources(sources=sources, needed_amt=needed_vol, **kwargs)
            
            for (curr_src, curr_vol) in water_sources.items():
                curr_src.contents, transferred = curr_src.remove(remove_volume=curr_vol)
                water_found |= transferred
                
                obtained_vol = sum((liquid.volume for liquid in water_found))
                # a bit ugly to use tuple unpacking here, but it should enforce the synchronization of transfer on both ends.
                if obtained_vol >= needed_vol: break # shouldn't really be necessary, but there's no harm in being a bit paranoid.
                
        water_pool = comestibles.Water(volume=obtained_vol) # to simplify things for now - merge the water pool instances.
        return water_pool
        
    def get_grounds(self, *args, **kwargs):
        """Handles the provision of coffee grounds for the extraction process. """
        
        sources = self.installed_components.get(const.COMP_BEANS)
        grinders = self.installed_components.get(const.COMP_GRINDER)
        
        if not sources: raise RuntimeError("Coffee bin not found!")
        if not grinders: raise RuntimeError("No operational bean grinder found!")
        
        beans = comestibles.CoffeeBeans(amount=100)
        
        grind_result = self.pick_grinder(grinders=grinders).grind(items={beans: beans.amount})
        
        grounds = grind_result.get(beans, {}).get(const.MAT_GROUNDS)
        
        return grounds
        
    def get_extract(self, grounds=None, medium=None, *args, **kwargs):
        """Handles the process of brewing a basic coffee bean extract - i.e. plain black coffee.
        
        :param grounds: brewable caffeine source
        :param medium: heatable liquid
        """
        if not (self.powered and grounds and medium): return medium
        
        heater = self.pick_heater(heaters=self.installed_components.get(const.COMP_HEATER))
        to_heat = [medium]
        heated = heater.heat(items=to_heat, target_temp=0.8*(const.WATER_EVAPORATE_PT-const.WATER_FREEZE_PT))
        heated = heated[medium]
        
        caffeine = grounds.extract() if grounds else NotImplemented
        
        brew = (heated if caffeine is NotImplemented 
                       else comestibles.Coffee(
                                               volume=heated.volume, 
                                               temperature=heated.temperature, 
                                               caffeine_content=caffeine,
                                               **kwargs)
                )
        return brew, grounds
        
    def get_extras(self, brew, *args, **kwargs):
        """Handles anything added to the coffee *in the brewing process*,
        e.g. (steamed) milk for white coffees, crema, etc.
        
        :param brew: basic extract to which extras are being added.
        """
        if not self.powered: return brew
        coffee = brew # just to make it explicit a transformation into the final product has occured.
        return coffee 
        
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
        
    def pick_bean_sources(self, sources, needed_amt, *args, **kwargs):
        """Handles selecting how much coffee to retrieve and from which source.
        
        :param sources: bean containers to choose from; Mapping of objects to stored volumes.
        :param needed_amt: numeric; the requested amount of beans.
        :returns: a dict of sources used and the amount of beans to obtain from each source.
        """
        remaining_amt = needed_amt
        solution = {}
        # very simple algorithm: greedily exhaust each source in the order of traversal
        # could be overridden in a subclass for a smarter protocol, e.g. try to empty out the tanks first.
        for src, vol in sources.items():
            used_amt = min(vol, remaining_amt)
            remaining_amt -= used_amt
            solution[src] = used_amt        
        return solution
        
    def pick_grinder(self, grinders, *args, **kwargs):
        """Handles selecting which grinder to use - and reconfiguring it if needed.
        
        :param grinders: grinders to choose from; Iterable.
        :returns: a selected grinder.
        """
        return next(iter(grinders)) if grinders else None # simple stub
        
    def pick_heater(self, heaters, *args, **kwargs):
        """Handles selecting which heater to use - and reconfiguring it if needed.
        
        :param heaters: heaters to choose from; Iterable.
        :returns: a selected heater.
        """
        return next(iter(heaters)) if heaters else None # simple stub
        
    def grounds_dispose(self, grounds, *args, **kwargs):
        if not self.powered: return grounds
        return None # magically evaporates the grounds
    
    
class GenericCoffeemaker(AbstractCoffeemaker):
    """An example using a non-specific, off-brand, made-up coffeemaker model 
    to demo the simulation functionality.
    """
    
    def __init__(self, turned_on=True, *args, **kwargs):
        """ """
        self.installed_components = {
            const.COMP_WATER : [water_supply.Tank(contents={comestibles.Water: water_supply.Tank.capacity}) 
                                for _ in range(self.component_slots.get(const.COMP_WATER, 0))],
                                
            const.COMP_BEANS : [bean_supply.Container() for _ in range(self.component_slots.get(const.COMP_BEANS, 0))],
            
            const.COMP_GRINDER : [grinders.Grinder() for _ in range(self.component_slots.get(const.COMP_GRINDER, 0))],
            
            const.COMP_HEATER : [heaters.Heater() for _ in range(self.component_slots.get(const.COMP_HEATER, 0))],
            
            # const.COMP_FILTER : [NotImplemented for _ in range(self.component_slots.get(const.COMP_FILTER, 0))],
            # const.COMP_GROUNDSBIN: [NotImplemented for _ in range(self.component_slots.get(const.COMP_GROUNDSBIN, 0))],
        }
        
        self.power_button = interfaces.PowerButton(owner=self, **kwargs)
        if turned_on: self.power_button.press()
        
        self.coffee_button = interfaces.CoffeeButton(owner=self, **kwargs)
    
Coffeemaker = GenericCoffeemaker # alias
