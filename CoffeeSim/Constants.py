# -*- coding: utf-8 -*-
"""String constants module. Fairly self-explanatory."""

DEFAULT_VOLUME = 100 # Physical volume, not sound volume!
USE_SOUND_EFFECTS = True

class Unlocalized(object):
    """Holds generic/shared/still-not-localized constants.
    Subclasses provide localization.
    """
    
    
    # Physics:
    TEMP_UNIT = 'Celsius'
    ROOMTEMP = 25
    ABS_ZERO = -273
    WATER_FREEZE_PT = 0
    WATER_EVAPORATE_PT = 100
    
    VOLUME = 'volume'
    VOLUME_UNIT = 'mL'
    
    # Temperature descriptions:
    WARMTH_FROZEN = "frozen"
    WARMTH_ICY = "ice-cold"
    WARMTH_COLD = "cold"
    WARMTH_MED = "lukewarm"
    WARMTH_WARM = "warm"
    WARMTH_HOT = "hot"
    WARMTH_BOILING = "boiling hot"
    
    # Strength:
    STRENGTH_DECAF = 'decaf'
    STRENGTH_LOW = 'mild' # because 'weak' is a negatively charged phrasing. Marketing, yay!
    STRENGTH_MEDIUM = 'medium-strength'
    STRENGTH_HIGH = 'strong'
    
    # Pressure:
    PRESSURE_LOW = 'low'
    PRESSURE_MEDIUM = 'medium'
    PRESSURE_HIGH = 'high'
    
    # Brew types:
    BREWTYPE_GENERIC = 'Coffee'
    BREWTYPE_ESPRESSO = 'Espresso'
    BREWTYPE_AMERICANO = 'Americano'
    BREWTYPE_CREMA = 'Caffe Crema'
    BREWTYPE_CAPPUCINO = 'Cappucino'
    
    # Extras keys:
    EXTRA_CREMA = 'crema'
    EXTRA_MILK = 'milk'
    EXTRA_MILKFOAM = 'steamed milk'
    
    # Component slots:
    COMP_WATER = 'Water Source'
    COMP_BEANS = 'Bean Supply'
    COMP_GRINDER = 'Bean Grinder'
    COMP_HEATER = 'Heating Element'
    COMP_FILTER = 'Filter'
    COMP_GROUNDSBIN = 'Grounds Disposal'
    
    # Raw materials:
    MAT_GROUNDS = 'coffee grounds'
    MAT_BEANS = 'coffee beans'
    
    # Localizations:
    LOC_LIQUID = 'liquid'
    LOC_WATER = 'water'
    LOC_COFFEE = 'coffee'
    
    LOC_PROGRAM_DESC = """Welcome to CoffeeSim! Let's make some coffee!"""
    
class PolishLocalization(Unlocalized):
    # just as a proof of concept:
    STRENGTH_LOW = 'łagodna'
    STRENGTH_MEDIUM = 'srednia'
    STRENGTH_HIGH = 'mocna'