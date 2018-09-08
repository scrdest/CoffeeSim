"""Main entrypoint to the coffeemaker simulation.

"""

from Constants import Unlocalized as const


def make_coffee(coffeemaker=None, *args, **kwargs):
    """Abstract, high-level coffeemaking interface.
    
    :param coffeemaker: optional; 
    """
    
    if not coffeemaker or coffeemaker is NotImplemented:
        from models.generic import GenericCoffeemaker
        coffeemaker = GenericCoffeemaker()
        
    coffee = coffeemaker.brew()
    
    return coffee
        

def main():
    return make_coffee()
    
    
if __name__ == '__main__': main()