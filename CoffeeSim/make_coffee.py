"""Main entrypoint to the coffeemaker simulation.

"""

import CoffeeSim.Constants as Constants
const = Constants.Unlocalized

def make_coffee(coffeemaker=None, preset=NotImplemented, *args, **kwargs):
    """Abstract, high-level coffeemaking interface.
    
    :param coffeemaker: optional; coffeemaker model to use
    :param preset: optional; preset to use (note: NOT guaranteed to be supported properly!)
    """
    if not coffeemaker or coffeemaker is NotImplemented:
        from CoffeeSim.models.generic import GenericCoffeemaker
        coffeemaker = GenericCoffeemaker()
        
    if preset is NotImplemented:
        options = getattr(coffeemaker, 'coffee_buttons', None) or tuple()
        if options:
            import random
            preset = getattr(random.choice(options), 'preset', None)
            
    coffee = coffeemaker.brew(preset=preset)
    print("\n~~ {coffee} ~~".format(coffee=coffee))
    
    return coffee
        

def main(*args, **kwargs):
    return serve_CLI(*args, **kwargs)
    
def serve_CLI(*args, **kwargs):
    import argparse
    
    coffee_maker_mapper = {
        'none': None,
        'generic': None, 
        'default': None,
    }
    
    preset_raw_mapper = {
        'none': None,
        'random': NotImplemented, 
        'default': None,
    }
    
    arg_parser = argparse.ArgumentParser(description=const.LOC_PROGRAM_DESC)
    arg_parser.add_argument('-C', '--coffeemaker', help="Optional. Coffeemaker model to use; supported: {opts} <case-insensitive>.".format(opts=tuple(coffee_maker_mapper.keys())))
    arg_parser.add_argument('-P', '--preset', help="Optional. Preset to use; supported: {opts} <case-insensitive>.".format(opts=tuple(preset_raw_mapper.keys())))
    arg_parser.add_argument('-q', '--quiet', action='store_true', help="Optional. Silences the sound effects.")
    arg_parser.add_argument('args', nargs='*', help="Optional; passed to the program as *args.")
    
    parsed_args = vars(arg_parser.parse_args())
    coffee_maker, args = None, tuple()
    
    if 'coffeemaker' in parsed_args: 
        coffee_maker_raw = parsed_args.pop('coffeemaker')
        
        coffee_maker = coffee_maker_mapper.get(coffee_maker_raw) or coffee_maker_mapper.get(str(coffee_maker_raw).lower(), NotImplemented)
        
        if coffee_maker is NotImplemented: print("WARNING: unrecognized coffeemaker '{}'. Using default coffeemaker as a fallback!"
                                                .format(coffee_maker_raw))
    if 'preset' in parsed_args: 
        preset_raw = parsed_args.pop('preset')
        
        used_preset = preset_raw_mapper.get(preset_raw) or preset_raw_mapper.get(str(preset_raw).lower(), NotImplemented)
        if coffee_maker is NotImplemented: print("WARNING: unspecified preset; a random available preset will be picked.")
        
    if 'quiet' in parsed_args and parsed_args.pop('quiet'): Constants.USE_SOUND_EFFECTS = False
        
    if 'args' in parsed_args: args = parsed_args.pop('args')
    
    make_coffee(coffee_maker, preset=used_preset, *args, **parsed_args)
    
if __name__ == '__main__': 
    main()
    