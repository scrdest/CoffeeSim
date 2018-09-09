import unittest

import os

loader = unittest.defaultTestLoader
runner = unittest.TextTestRunner()

curr_dir = os.path.abspath(os.path.dirname(__file__))
top_level = os.path.join(os.path.dirname(curr_dir))

discovered = loader.discover(start_dir=curr_dir, top_level_dir=top_level)

print("x="*34 + 'x')
print("Initiating tests...")
print("")
runner.run(discovered)
