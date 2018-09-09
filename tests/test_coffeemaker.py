"""Tests to verify high-level performance of the coffee machines as a whole."""

import unittest 

from CoffeeSim.make_coffee import make_coffee

from CoffeeSim.models import generic

def handle_IO(*args, **kwargs): print(*args, **kwargs)

class AbstractBrewingInterfaceTest(unittest.TestCase):
    """Tests whether the generic, model-agnostic brewing API produces coffee for a specified model."""
    
    def case_spec(self, coffeemaker, *args, **kwargs): # yes, I am THAT lazy
        """Generates test cases for individual coffeemaker models.
        
        :param coffeemaker: a configured *INSTANCE* of a coffee machine
        """ 
        brewed = make_coffee(coffeemaker, *args, **kwargs)
        self.assertIsNotNone(brewed)
        handle_IO("")
        handle_IO("{coffm} input passed all tests!\n".format(coffm=type(coffeemaker).__name__))
            
    def test_default(self): return self.case_spec(coffeemaker=None)
        
    def test_generic(self): return self.case_spec(coffeemaker=generic.GenericCoffeemaker())


class GenericCoffeemakerIntegrationTest(unittest.TestCase):
    """Tests whether the GenericCoffeemaker brews coffee as expected in the happy case."""
    def setUp(self):
        self.machine = generic.GenericCoffeemaker(turned_on=False)
    
    def test_power_button(self):
        """Verifies a full power cycle is possible to execute using the machine's power button."""
        state_checks = (self.assertTrue, self.assertFalse)
        if self.machine.powered: state_checks = tuple(reversed(state_checks))
        
        for checker in state_checks:
            self.machine.power_button.press()
            checker(self.machine.powered)
        else: handle_IO("\nAll power button responses working as expected.")
            
    def test_power_required(self):
        """Verifies power is required to use the machine."""
        self.machine.powered = False
        self.assertIsNone(self.machine.brew())
    
    def test_brewing(self):
        self.machine.powered = True
        brew = self.machine.brew()
        self.assertIsNotNone(brew)
        
def main(): return unittest.main()
        
if __name__ == '__main__': main()