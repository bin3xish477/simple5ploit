# simple5ploit
`simple5ploit` is an exploitation/information gathering framework designed for Python3 scripts. `simple5ploit` was created as a contribution focused project which is why is doesn't provide many modules by default. I wanted to create a tool that anyone who knows basic Python can contribute to (check out the other sections of this README file). Most of the exploits being written today are in Python so I thought it would be awesome to create a tool to manage these Python exploits. `simple5ploit` allows users to easily select and use exploits like the well-known `msfconsole` exploitation tool. 

### Setup

```
python3 -m pip install -r requirements.txt
```

### Simple5ploit's Interface

Show images of simple5ploit here!!!
- show autocompletion
- show table output from help, info, and show commands

### Contributing to Simple5ploit

1. Fork simple5ploit's repo
2. Watch this [video](https://www.youtube.com/watch?v=nT8KGYVurIU) on how to fork and make pull requests if you don't know how to do so already
3. Make a pull request with your exploit or gather module and I'll add your exploit or gather module to simple5ploit

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
        {
          "description": "an argument for this example exploit class",
          "required": True }
    }
    
    # initializing class variables for exploit arguments with values set to `N/a`
    # ::they could also be set to empty string
    for arg in self.args:
      self.__dict__[arg] = "N/a"
      
  def run(self):
    """
    This function is where the exploit code should be placed.
    If it's not implemented, a ```NotImplementedError``` will be raised.
    """
    pass
    
# ***************************************************************************************************
    
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
        {
          "description": "an argument for this example gather module class",
          "required": True }
    }
    
    # initializing class variables for script arguments with values set to `N/a`
    # ::they could also be set to empty string
    for arg in self.args:
      self.__dict__[arg] = "N/a"
      
  def run(self):
    """
    This function is where the code for this gather module should be placed.
    If it's not implemented, a ```NotImplementedError``` will be raised.
    """
    pass
```

### Simple5ploit Server

Quickly launch a Python HTTP server with:

```
simple5plit -s [port]
```
