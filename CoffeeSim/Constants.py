# -*- coding: utf-8 -*-
"""String constants module. Fairly self-explanatory."""

class Unlocalized(object):
    """Holds generic/shared/still-not-localized constants.
    Subclasses provide localization.
    """
    
    DEFAULT_VOLUME = 100
    
    # Physics:
    TEMP_UNIT = 'Celsius'
    ROOMTEMP = 25
    ABS_ZERO = -273
    WATER_FREEZE_PT = 0
    WATER_EVAPORATE_PT = 100
    
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
    STRENGTH_MEDIUM = 'medium'
    STRENGTH_HIGH = 'strong'
    
    # Brew types:
    BREWTYPE_ESPRESSO = 'Espresso'
    BREWTYPE_AMERICANO = 'Americano'
    BREWTYPE_CREMA = 'Caffe Crema'
    BREWTYPE_CAPPUCINO = 'Cappucino'
    
    # Component slots:
    COMP_WATER = 'Water Source'
    COMP_BEANS = 'Bean Supply'
    COMP_GRINDER = 'Bean Grinder'
    COMP_HEATER = 'Heating Element'
    COMP_FILTER = 'Filter'
    COMP_GROUNDSBIN = 'Grounds Disposal'
    
class PolishLocalization(Unlocalized):
    # just as a proof of concept:
    STRENGTH_LOW = 'łagodna'
    STRENGTH_MEDIUM = 'srednia'
    STRENGTH_HIGH = 'mocna'