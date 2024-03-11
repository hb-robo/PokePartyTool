from abc import ABC, abstractmethod
import pandas as pd
import 

pokeDex = pd.read_csv('data/rby/rby_pokedex.csv', index_col='mon_name')

"""
Refactor of the "classes.py" Monster class, to work with JSON data that resembles a Pokedex entry.
Only serves as a 
"""


class Pokemon(ABC):
    
    def __init__(self, name, level=50):
        self.name = name
        self.level = level
        
        
        dex_entry = self.getDexEntry(name)
        dex_entry = pokedex[name]
        
        self.name = name
        self.level = level
        self.type1, self.type2 = dex_entry.types
        self.stats = self.default_stats = dex_entry.stats
        
    
    def getDexEntry(name, pokedex):
        # implemented on a per-game level to account for differences in poxedexes.
        raise NotImplementedError("This method should be defined by subclasses.")
    
    
    @abstractmethod
    def uses(self):
        pass
    
    @abstractmethod
    def
    