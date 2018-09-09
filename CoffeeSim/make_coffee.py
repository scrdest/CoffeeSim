"""Main entrypoint to the coffeemaker simulation.

"""

import CoffeeSim.Constants as Constants
const = Constants.Unlocalized

def make_coffee(coffeemaker=None, *args, **kwargs):
    """Abstract, high-level coffeemaking interface.
    
    :param coffeemaker: optional; 
    """
    
    if not coffeemaker or coffeemaker is NotImplemented:
        from CoffeeSim.models.generic import GenericCoffeemaker
        coffeemaker = GenericCoffeemaker()
        
    coffee = coffeemaker.brew()
    print("\n~~ {coffee} ~~".format(coffee=coffee))
    
    return coffee
        

def main(*args, **kwargs):
    return serve_CLI(*args, **kwargs)
    
def serve_CLI(*args, **kwargs):
    import argparse
    
    arg_parser = argparse.ArgumentParser(description=const.LOC_PROGRAM_DESC)
    #arg_parser.add_argument()
    
    parsed_args = vars(arg_parser.parse_args())
    
    make_coffee(**parsed_args)
    
if __name__ == '__main__': 
    main()
    