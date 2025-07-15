from __future__ import annotations
from typing import List, Dict
from classes.treepatch_sub_class import Treepatch
from classes.landpatch_base_class import Landpatch
import random

""" The Firefighter Class:

    Represents a firefighter in a forest simulation. Firefighters can move, extinguish fires, and have a skill level for fire extinguishing.

    Firefighter Movement:
    - Firefighters can move only once per evolution step.
    - They will move randomly to a neighboring patch if not involved in extinguishing a fire or if no fires are burning in an adjacent patch.
    - If a fire is in an adjacent patch, they will move to the neighboring burning patch.

    Attributes:
        _firefighter_id (int): The unique identifier for the firefighter.
        __avg_skill (int): The skill level of the firefighter for extinguishing fires.
    Note: id is protected and avg skill is private.

    Methods:
        __init__(self, firefighter_id: int, avg_skill: int) -> None:
            Initializes a Firefighter instance with a given firefighter ID and average skill level.

        fight_fire(self, treepatch: Treepatch) -> None:
            Attempts to extinguish a fire in the provided Treepatch based on the firefighter's skill level.

        move(self, landpatch: Landpatch, firefighter_positions: List[int]) -> int:
            Determines the next position for the firefighter to move based on neighboring patches and ongoing fires.

        get_avg_skill(self) -> int:
            Returns the average skill level of the firefighter for extinguishing fires.
    Note: All methods are public. """

class Firefighter:
    def __init__(self:Firefighter,
                 firefighter_id:int,
                 avg_skill:int) -> None:
        
        self.__avg_skill = avg_skill
        self._firefighter_id = firefighter_id
    
    def fight_fire(self, treepatch:Treepatch) -> None:
        """ Attempt to extinguish a fire in the provided Treepatch based on the firefighter's skill level.
        
        Args:
            treepatch (Treepatch): The Treepatch node to extinguish the fire on. """       
        if not treepatch.get_lit_state():
            return
        
        tree_stats = treepatch.get_tree_stats()
        if tree_stats + self.__avg_skill <= 256:
            treepatch.set_tree_stats(tree_stats + self.__avg_skill)
        else:
            treepatch.set_tree_stats(256)

    def move(self, landpatch:Landpatch, firefighter_positions:List[int]) -> int:
        """ Determine the next position for the firefighter to move based on neighboring patches and ongoing fires.

        Args:
            landpatch (Landpatch): The current Landpatch the firefighter is on.
            firefighter_positions (List[int]): The list of positions occupied by other firefighters.
        Returns:
            int: The next position for the firefighter to move to. """       
        neighbours:Dict[int, Landpatch] = landpatch.get_neighbors()
        for landpatch in neighbours.values():
            if isinstance(landpatch, Treepatch):
                if landpatch.get_lit_state() and not landpatch.get_patch_id() in firefighter_positions:
                    return landpatch.get_patch_id()
        
        destination = random.choice(list(landpatch.get_neighbors_id()))
        while destination in firefighter_positions:
            destination = random.choice(list(landpatch.get_neighbors_id()))
        
        return destination

    def get_avg_skill(self) -> int:
        """ Return the average skill level of the firefighter for extinguishing fires.

        Returns:
            int: The average skill level. """       
        return self.__avg_skill