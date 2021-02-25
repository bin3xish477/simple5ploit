# simple5ploit
An exploitation framework designed for Python3 scripts

### Setup

```
python3 -m pip install -r requirements.txt
```

### Creating an Exploit/Gather Module


```python

"""
-------------------------------
EXPLOIT MODULE EXAMPLE
-------------------------------
"""
# importing the parent exploit class
from modules.exploits.internal.base import Exploit

# defining an exploit module class
class SomeExploit(Exploit):
  def __init__(self):
    # exploit module custom prompt
    self.prompt = "[CustomExploitPrompt] :> "
    
    # exploit module information dict
    self.info = {
      "Author": "Alexis Rodriguez",
      "Description": "An example exploit class"
    }
    
    # exploit module arguments dict
    self.args = {
      "some_argument":
        "description": "an argument for this example exploit class",
        "required": True
    }
    
    # initializing class variables for exploit arguments with values set to `N/a`
    # ::they could also be set to empty string
    for arg in self.args:
      self.__dict__[arg] = "N/a"
      

"""
----------------------------
GATHER MODULE EXAMPLE
----------------------------
"""
# importing the parent gather module class
from modules.gather.internal.base import Gather

# defining a gather module class
class SomeGatherModule(Gather):
  def __init__(self):
    # gather module custom prompt
    self.prompt = "[CustomPrompt] % "
    
    # gather module information dict
    self.info = {
      "Author": "Alexis Rodriguez",
      "Description": "An example informating gather module class"
    }
    
    # gather module arguments dict
    self.args = {
      "some_argument":
        "description": "an argument for this example gather module class",
        "required": True
    }
    
    # initializing class variables for script arguments with values set to `N/a`
    # ::they could also be set to empty string
    for arg in self.args:
      self.__dict__[arg] = "N/a"
```
