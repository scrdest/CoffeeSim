CoffeeSim
===========
A grossly OOP simulation of a coffee machine.

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



Overview:
-----------
