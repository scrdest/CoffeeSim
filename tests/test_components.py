"""Tests to verify performance of the machine parts."""

import unittest 

from CoffeeSim.components import water_supply, bean_supply, grinders, heaters, interfaces

def handle_IO(*args, **kwargs): print(*args, **kwargs)


class WaterSupplyTest(unittest.TestCase):

    def test_watertank(self):
        empty_tank = water_supply.Tank(contents=None)
        
        # Empty tank acts empty:
        self.assertFalse(empty_tank.contents)
        self.assertEquals(empty_tank.contents_volume, 0)
        with self.assertRaises(RuntimeWarning): self.assertEquals(empty_tank.remove(10), 10)
        print("\nEmpty tank behavior as expected...")
    
    
class BeanSupplyTest(unittest.TestCase):

    def test_container(self):
        pass
    
    
class GrinderTest(unittest.TestCase):

    def test_base_grinder(self):
        pass
    
    
class HeaterTest(unittest.TestCase):

    def test_base_heater(self):
        pass
    
    
        
        
def main(): return unittest.main()
        
if __name__ == '__main__': main()