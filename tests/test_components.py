"""Tests to verify performance of the machine parts."""

import unittest 

from CoffeeSim.components import water_supply, bean_supply, grinders, heaters, interfaces

from CoffeeSim import comestibles

def handle_IO(*args, **kwargs): print(*args, **kwargs)


class WaterSupplyTest(unittest.TestCase):

    def test_empty_watertank(self):
        empty_tank = water_supply.Tank(contents=None)
        
        # Empty tank acts empty:
        self.assertFalse(empty_tank.contents)
        self.assertEquals(empty_tank.contents_volume, 0)
        with self.assertRaises(RuntimeWarning): self.assertEquals(empty_tank.remove(10), 10)
        print("\nEmpty tank behavior as expected...")

    def test_filled_watertank(self):
        contents_to_use = {comestibles.Water: water_supply.Tank.capacity}
        tank = water_supply.Tank(contents=contents_to_use)
        
        # Volume detected:
        self.assertTrue(tank.contents)
        self.assertGreater(tank.contents_volume, 0)
        for cont_type, volume in contents_to_use.items():
            # nasty bit of O(n^2)... sadly necessary, because item contents are instances while we pass in classes as args
            if volume > 0: self.assertTrue(any((isinstance(cont, cont_type) for cont in tank.contents)))
        with self.assertRaises(RuntimeWarning): tank.fill(contents_to_use)
        print("\nFilled tank behavior as expected...")
    
    
class BeanSupplyTest(unittest.TestCase):

    def test_container(self):
        container = bean_supply.Container()
    
    
class GrinderTest(unittest.TestCase):

    def test_base_grinder(self):
        grinder = grinders.Grinder()
        empty_run = grinder.grind(items=None)
        self.assertFalse(empty_run)
        print("\nGrinder behavior as expected...")
    
    
class HeaterTest(unittest.TestCase):

    def test_base_heater(self):
        heater = heaters.Heater()
        empty_run = heater.heat(items=None)
        self.assertFalse(empty_run)
        print("\nHeater behavior as expected...")
        
        
        
def main(): return unittest.main()
        
if __name__ == '__main__': main()