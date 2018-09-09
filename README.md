CoffeeSim
===========
A grossly OOP simulation of a coffee machine.

Requirements:
-----------

- Python (tested on CPython: 2.7, 3.5.3, 3.7)
- That's it!

________

Quickstart:
-----------

### CLI:
`python -m CoffeeSim (-C <coffeemaker string>, -P <preset string>) | -h (help)`

Or:
`python make_coffee.py (-C <coffeemaker string>, -P <preset string>) | -h (help)`

### From within Python:

#### Abstract interfaces:
```
# Broadest, declarative-ish API:
from CoffeeSim.make_coffee import make_coffee
elixir_of_life = make_coffee()
```

```
# Object-oriented API:
from CoffeeSim.models.generic import Coffeemaker # (or another machine model)
coffeemaker = Coffeemaker()
cup_of_liquid_code = coffeemaker.brew()
```

#### Simulated physical interfaces:
```
import random
from CoffeeSim.models.generic import Coffeemaker # (or another machine model)
coffeemaker = Coffeemaker()
another_baroque_description = random.choice(coffeemaker.coffee_buttons).press()
# note: the above example does NOT validate that there are any buttons or handle such a case
```

#### Run all tests:
`python -m tests`

Overview:
-----------

### Coffeemaker

The Coffeemaker class is a high-level abstraction encapsulating the *user-facing functionality* of the coffee machine.

This includes features such as brewing the actual coffee, managing the components and routing resources, 
providing hooks to handle various extra functionalities such as foaming milk for cappucinos, 
and exposing its physical interface elements (that is, simulations of hardware buttons).

This does NOT include functionalities such as grinding the beans - as far as the machine is concerned,
its job is to delegate the provision of the grounds to the appropriate component, or to signal their unavailability.

Likewise, the physical interface functionalities themselves are also handled within the Buttons - the machine just signals they are there.

NOTE: remember - electronics tend to work best powered on... The default implementation starts turned on unless specified, but a subclass may not violate that assumption.

#### API conventions:

- get_FOO() functions provide managed resource (water, beans, etc.) access
- pick_FOO() functions handle dispatching resources from resource pools
- dispose_FOO() functions hand off resources outside the object scope (transfer/delete operations)
- handle_FOO() functions provide hooks & customized handling *WITHIN* the realm of the concerns of the abstraction

_______

### Components:

The Components package classes declare the available slots for various components. 

This enables models such as, say, a coffee machine connected to the hydraulics plus a reserve water tank, or multiple tanks.
The actual components are populated on __init__.

The components provide lower-level abstractions as appropriate, e.g.: 
- a Grinder exposes a grinding API, 
- a Heater exposes an API for heating the provided items, 
- a (water) Tank or a (coffee) Container provides functions to fetch and refill its contents,
...and so on.

Note that the separation of levels of abstraction is, once again, maintained - a Grinder may call grind() on its targets,
but ultimately it's the targets themselves that decide how to respond to being ground.

The Button component and its children in the interfaces module is something of an oddball: rather than having a set API,
its instances have to register a callback and a weak reference to the owner - the physical interface holder.
This enables the maintenance of decoupling of functionality from the implementation while still providing the access to holder state.

_______

### Resource types:

A coffee machine that does not make coffee is quite a tragic sight. As such, the drink itself, and the raw materials needed to make it
also need proper abstractions - which are provided by comestibles module.

The primary classes included are Liquid and CaffeineSource. 

**Liquid** provides some simple, pseudo-volumetric-ish logic and very basic physics, plus dynamically generated string representations/descriptions.
Two classes inheriting from it are Water and Coffee.

**CaffeineSource** represents solids - coffee beans, coffee grounds, possibly pre-ground capsules, instant coffee or cocoa.
All CaffeineSources expose an extract() method to yield a percentage of their caffeine content, although the efficiency of the process may vary.

In addition, CoffeeBeans expose a grind() method, which may be used to turn them into CoffeeGrounds - currently only used by the Grinder component,
but there's nothing standing in the way of, say, implementing grinding them by hand.

_______

### Presets:

Many self-service-oriented coffee machines provide some kind of user-friendly, predefined configuration that facilitates making a decent
cup of whichever kind of coffee you pick without too much hassle or specialized knowledge.

The classes defined in the modules comprising the Presets package model these kinds of configurations.

A preset may define a volume, strength, brewing pressure, any extras (things beyond plain black coffee; e.g. milk foam) and name override for the brew.
Note that these override the coffeemaker defaults where applicable and supported, but are overruled by the *user's* configuration options.

For example, picture the following scenario: a User presses the Espresso button on the machine and sets the volume to 300 mL.
The logic determining the volume goes as follows:

(default coffee volume: 100 mL) --|overruled by Preset|--> (Espresso preset volume: 20 mL) --|overruled by User|--> (User-defined volume: 300 mL) ==> 300 mL of Espresso

_______


