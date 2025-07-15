from __future__ import annotations
from typing import Dict
from classes.landpatch_base_class import Landpatch
import classes.treepatch_sub_class
import random

""" Rock Patch Dynamics:

    Each Rockpatch has a possibility of becoming a Treepatch at each step (default 1%).
    Like the Treepatch class, the Rockpatch class is also a subclass of the Landpatch Class and implements the abstract methods defined in the class contract.

    Attributes:
        patch_id (int): The unique identifier for the Rockpatch.
        neighbors (Dict[int, Landpatch]): A dictionary of neighboring landpatches.
        __prob_treepatch (float): The probability of becoming a Treepatch at each step (default 0.1).
        __patch_type (int): The type identifier for the Rockpatch (0 for Rockpatch).
    self.set_color(None): Sets the color the None (grey).
        
    Methods:
        mutate(self) -> Landpatch: Abstract method defined in the LandPatch class contract.
        update(self) -> bool: Abstract method defined in the LandPatch class contract.
        get_patch_type(self) -> int: Returns the type identifier of the Rockpatch (0 for Rockpatch).
        get_prob_treepatch(self) -> float: Returns the probability of becoming a Treepatch at each step.
    Note: Class properties are private. All class methods are public.
    """

class Rockpatch(Landpatch):
    def __init__(self:Rockpatch,
                 patch_id:int,
                 neighbors:Dict[int, Landpatch],
                 prob_treepatch=0.1) -> None:
        
        """ Initialize a Rockpatch instance.

        Args:
            patch_id (int): The unique identifier for the Rockpatch.
            neighbors (Dict[int, Landpatch]): A dictionary of neighboring landpatches.
            prob_treepatch (float): The probability of becoming a Treepatch at each step (default 0.1). """
        
        super(Rockpatch, self).__init__(patch_id, neighbors)
        
        self.__patch_type = 0
        self.__prob_treepatch = prob_treepatch
        self.set_color(None)

    def mutate(self) -> Landpatch:
        """ Return a new Treepatch instance as a result of the Rockpatch mutation. """       
        treepatch = classes.treepatch_sub_class.Treepatch(self.get_patch_id(), self.get_neighbors(), False)
        treepatch.set_tree_stats(1)
        return treepatch
    
    def update(self) -> bool:
        """ Update the state of the Rockpatch for each iteration of the simulation steps.

        Returns:
            bool: True if the Rockpatch should mutate into a Treepatch, False otherwise. """      
        if random.randint(1, 100) <= self.__prob_treepatch:
            return True
        return False

    def get_patch_type(self) -> int:
        """ Return the type identifier of the Rockpatch (0 for Rockpatch). """
        return self.__patch_type
                                               
    def get_prob_treepatch(self) -> float:
        """ Return the probability of becoming a Treepatch at each step. """
        return self.__prob_treepatch