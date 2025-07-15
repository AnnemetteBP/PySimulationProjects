from __future__ import annotations
from typing import List, Dict,Tuple, Optional
from abc import ABC, abstractmethod

""" The Landpatch Abstract Class:

    Landpatch Representation:
    Manages landpatches (Treepatches and Rockpatches) for the Land class.

    Object-Oriented Design:
    Implements an object-oriented representation.
    Implements the class structure with a base class (Landpatch) and two subclasses (Treepatch and Rockpatch).

    Attributes:
        _patch_id (int): The unique identifier for the landpatch.
        _neighbors (Dict[int, Landpatch]): A dictionary of neighboring landpatches.
        _position (Tuple[float, float]): The position of the landpatch on the graph.
        _color (int): The color of the landpatch.
        _firefighter (bool): A boolean indicating the presence of a firefighter on the landpatch.
    Note: All properties are protected.

    Methods:
        get_patch_id(self) -> int: Returns the unique identifier of the landpatch.
        set_patch_id(self, patch_id: int) -> None: Sets the unique identifier of the landpatch.
        get_position(self) -> Tuple[float, float]: Returns the position of the landpatch.
        set_position(self, position: Tuple[float, float]) -> None: Sets the position of the landpatch.
        get_color(self) -> int: Returns the color of the landpatch.
        set_color(self, color: int) -> None: Sets the color of the landpatch.
        has_firefighter(self) -> bool: Returns True if a firefighter is present on the landpatch, False otherwise.
        set_firefighter(self, has_firefighter: bool) -> None: Sets the presence of a firefighter on the landpatch.
        get_neighbors(self) -> Dict[int, Landpatch]: Returns the dictionary of neighboring landpatches.
        get_neighbors_id(self) -> List[int]: Returns the IDs of neighboring landpatches.
        set_neighbors(self, neighbors: Dict[int, Landpatch]) -> None: Sets the neighboring landpatches.
        add_landpatch_to_neighbour(self: Landpatch, new_neighbour: Landpatch) -> None: Adds a new neighboring landpatch.
        remove_landpatch_to_neighbour(self: Landpatch, patch_id_to_remove: int) -> None: Removes a neighboring landpatch.
    Note: All methods are public.

    Abstract Methods:
        mutate(self) -> Landpatch: Allows swapping a Treepatch with a Rockpatch without losing connections to neighbors and associations with firefighters.
        update(self) -> bool: Updates the state of the landpatch for each iteration of the simulation steps. Returns True if the landpatch should mutate.
    Note: The abstract methods are implemented by the subclasses Treepatch and Landpatch. """

class Landpatch(ABC):
    def __init__(self,
                 patch_id:int,
                 neighbors:Dict[int, Landpatch] = {},
                 position:Optional[Tuple] = (0.0, 0.0),
                 color:Optional[int] = 0,
                 firefighter:Optional[bool] = False) -> None:
        
        """ Initialize a Landpatch instance.

        Args:
            patch_id (int): The unique identifier for the landpatch.
            neighbors (Dict[int, Landpatch]): A dictionary of neighboring landpatches.
            position (Optional[Tuple]): The position of the landpatch on the graph. Defaults to (0.0, 0.0).
            color (Optional[int]): The color of the landpatch. Defaults to 0.
            firefighter (Optional[bool]): A boolean indicating the presence of a firefighter. Defaults to False. """
        
        self._patch_id = patch_id
        self._neighbors = neighbors
        self._position = position
        self._color = color
        self._firefighter = firefighter

    """ Getters and Setters. """
    def get_patch_id(self) -> int:
        return self._patch_id
    
    def set_patch_id(self, patch_id:int) -> None:
        self._patch_id = patch_id

    def get_position(self) -> Tuple[float, float]:
        return self._position
    
    def set_position(self, position:Tuple[float, float]) -> None:
        self._position = position

    def get_color(self) -> int:
        return self._color
    
    def set_color(self, color:int) -> None:
        self._color = color

    def has_firefighter(self) -> bool:
        return self._firefighter
    
    def set_firefighter(self, has_firefighter:bool) -> None:
        self._firefighter = has_firefighter
        
    def get_neighbors_id(self) -> List[int]:
        return self._neighbors.keys()

    def get_neighbors(self) -> Dict[int, Landpatch]:
        return self._neighbors
    
    def set_neighbors(self, neighbors:Dict[int, Landpatch]) -> None:
        self._neighbors = neighbors

    def add_landpatch_to_neighbour(self:Landpatch, new_neighbour:Landpatch) -> None:
        self._neighbors[new_neighbour.get_patch_id()] = new_neighbour

    def remove_landpatch_to_neighbour(self:Landpatch, patch_id_to_remove:int) -> None:
        del self._neighbors[patch_id_to_remove]
    
    @abstractmethod
    def mutate(self) -> Landpatch:
        """ Allows swapping a Treepatch with a Rockpatch without losing connections to neighbors and associations with firefighters. """
        pass

    @abstractmethod
    def update(self) -> bool:
        """Updates the state of the landpatch for each iteration of the simulation steps.

        Returns:
            bool: True if the landpatch should mutate, False otherwise. """
        pass