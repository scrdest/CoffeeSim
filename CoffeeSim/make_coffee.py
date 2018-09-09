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
    arg_parser.add_argument('-C', '--coffeemaker')
    arg_parser.add_argument('args', nargs='*')
    
    parsed_args = vars(arg_parser.parse_args())
    coffee_maker, args = None, tuple()
    
    if 'coffeemaker' in parsed_args: 
        coffee_maker_raw = parsed_args.pop('coffeemaker')
        
        coffee_maker_mapper = {
            'none': None,
            'generic': None, 
            'default': None,
        }
        
        coffee_maker = coffee_maker_mapper.get(coffee_maker_raw) or coffee_maker_mapper.get(str(coffee_maker_raw).lower(), NotImplemented)
        if coffee_maker is NotImplemented: print("WARNING: unrecognized coffeemaker '{}'. Using default coffeemaker as a fallback!"
                                                .format(coffee_maker_raw))
        
    if 'args' in parsed_args: args = parsed_args.pop('args')
    
    make_coffee(coffee_maker, *args, **parsed_args)
    
if __name__ == '__main__': 
    main()
    