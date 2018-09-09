import CoffeeSim.Constants as Constants
const = Constants.Unlocalized

class Preset(object):
    """A specification of configuration for a specific type of coffee."""
    output_name = const.BREWTYPE_GENERIC
    volume = Constants.DEFAULT_VOLUME
    pressure = const.PRESSURE_MEDIUM
    strength = const.STRENGTH_MEDIUM
    extras = tuple()

    
class GenericPreset(Preset): pass # child instead of alias to facilitate monkey-patching etc.


class Americano(GenericPreset):
    output_name = const.BREWTYPE_AMERICANO
    volume = 1.5 * Constants.DEFAULT_VOLUME
    pressure = const.PRESSURE_LOW
    strength = const.STRENGTH_LOW

    
class Crema(GenericPreset):
    output_name = const.BREWTYPE_CREMA
    volume = Constants.DEFAULT_VOLUME
    pressure = const.PRESSURE_MEDIUM
    strength = const.STRENGTH_MEDIUM
    extras = (const.EXTRA_CREMA,)

    
class Espresso(GenericPreset):
    output_name = const.BREWTYPE_ESPRESSO
    volume = 0.2 * Constants.DEFAULT_VOLUME
    pressure = const.PRESSURE_HIGH
    strength = const.STRENGTH_HIGH
    
    
class Cappucino(Espresso):
    output_name = const.BREWTYPE_CAPPUCINO
    volume = 0.8 * Constants.DEFAULT_VOLUME
    pressure = const.PRESSURE_HIGH
    strength = const.STRENGTH_MEDIUM
    extras = (const.EXTRA_MILKFOAM,)
