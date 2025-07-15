from __future__ import annotations
from typing import Dict
from classes.landpatch_base_class import Landpatch
import classes.rockpatch_sub_class
import random

""" Treepatch Dynamics:

    Tree patches will increase their treestats by a fixed amount each step if no fire is lit on the patch (+10).
    If a Treepatch is on fire, its treestats will decrease each step by a fixed amount (−20).
    If a Treepatch has treestats < 0, it mutates into a Rockpatch.
    If fire is burning in a Treepatch it can spread to any adjacent Treepatch with fixed probability (default 30%) 
    Instance Variable: treestats - Identifies the health of the Treepatch [0-256].

    Attributes:
        __patch_id (int): The unique identifier for the Treepatch.
        __neighbors (Dict[int, Landpatch]): A dictionary of neighboring landpatches.
        __lit_state (bool): A boolean indicating whether the Treepatch is on fire.
        __prob_autcombustion (float): The probability of spontaneous combustion (default 0.1).
        __tree_stats_max (int): The maximum value for treestats (default 256).
        __tree_stats_min (int): The minimum value for treestats (default 0).
        __tree_stats (int): The current health of the Treepatch.
    Note: All properties are private.  
        self.set_color(256): Sets color to green color scale.

    Methods:
        mutate(self) -> Landpatch: Abstract method defined in the Landpatch class contract.
        update(self) -> bool: Abstract method defined in the Landpatch class contract.
        get_patch_type(self) -> int: Returns the type identifier of the Treepatch (1 for Treepatch).
        get_prob_autcombustion(self) -> float: Returns the probability of spontaneous combustion.
        get_lit_state(self) -> bool: Returns True if the Treepatch is on fire, False otherwise.
        get_tree_stats(self) -> int: Returns the current health of the Treepatch.
        set_tree_stats(self, stats: int) -> None: Sets the health of the Treepatch.
        set_lit_state(self, state: bool) -> None: Sets the on-fire state of the Treepatch.
    Note: All methods are public. """

class Treepatch(Landpatch):
    def __init__(self:Treepatch,
                 patch_id:int,
                 neighbors:Dict[int, Landpatch],
                 lit_state:bool,
                 prob_autcombustion:float = 0.1) -> None:
        
        """ Initialize a Treepatch instance.

        Args:
            patch_id (int): The unique identifier for the Treepatch.
            neighbors (Dict[int, Landpatch]): A dictionary of neighboring landpatches.
            lit_state (bool): A boolean indicating whether the Treepatch is on fire.
            prob_autcombustion (float): The probability of spontaneous combustion (default 0.1). """
        
        super(Treepatch, self).__init__(patch_id, neighbors)
        
        self.__patch_type = 1
        self.__prob_autcombustion = prob_autcombustion
        self.__lit_state = lit_state
        self.__tree_stats_max = 256
        self.__tree_stats_min = 0
        self.__tree_stats = self.__tree_stats_max
        self.set_color(256)

    def mutate(self) -> Landpatch:
        """ Return a new Rockpatch instance as a result of the Treepatch mutation. """

        rockpatch = classes.rockpatch_sub_class.Rockpatch(self.get_patch_id(), self.get_neighbors())
        return rockpatch
    
    def update(self) -> bool:
        """ Update the state of the Treepatch for each iteration of the simulation steps.

        Returns:
            bool: True if the Treepatch should mutate, False otherwise. """     
        if random.randint(1, 100) <= self.__prob_autcombustion:
            self.__lit_state = True

        if not self.__lit_state:
            if self.__tree_stats + 10 <= self.__tree_stats_max:
                self.__tree_stats = self.__tree_stats + 10
            else:
                self.__tree_stats = self.__tree_stats_max
            self.set_color(self.__tree_stats)
        else:
            if self.__tree_stats - 20 >= self.__tree_stats_min:
                self.__tree_stats = self.__tree_stats - 20
                self.set_color(-256 - (-1 * self.__tree_stats))
            else:
                return True

        return False

    def get_patch_type(self) -> int:
        """ Return the type identifier of the Treepatch (1 for Treepatch). """
        return self.__patch_type
    
    def get_prob_autcombustion(self) -> float:
        """ Return the probability of spontaneous combustion. """
        return self.__prob_autcombustion
    
    def get_lit_state(self) -> bool:
        """ Return True if the Treepatch is on fire, False otherwise. """
        return self.__lit_state
    
    def get_tree_stats(self) -> int:
        """ Return the current health of the Treepatch. """
        return self.__tree_stats
    
    def set_tree_stats(self, stats:int) -> None:
        """ Set the health of the Treepatch. """      
        self.__tree_stats = stats
        if self.__tree_stats >= self.__tree_stats_max:
            self.__tree_stats = self.__tree_stats_max
            self.set_lit_state(False)

    def set_lit_state(self, state:bool) -> None:
        """ Set the on-fire state of the Treepatch. """
        self.__lit_state = state