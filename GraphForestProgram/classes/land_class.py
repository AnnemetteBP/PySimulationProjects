from __future__ import annotations
from typing import List, Dict,Tuple
import random
from classes.landpatch_base_class import Landpatch
from classes.treepatch_sub_class import Treepatch
from classes.config_class import Config
from classes.firefighter_class import Firefighter
from classes.graph_builder_class import GraphBuilder
import vis_modules.graph_helper as vh

""" The Land Class:

    Utilizes the provided module graph_helper to validate the structure with vh.edges_planar(List[Tuple[int,int]]).
        Ensures that the graph is planar by checking if the edges cross or not.
        If the edges do not cross and is otherwise connected, the graph can be validated as an accaptable input.
    Utilizes our own module graph_builder_class to validate validate if the graph nodes (vertices) are connected appropriately by edges.

    Attributes:
        __configs (Config): Configuration settings for the simulation.
        __land_patches (Dict[int, Landpatch]): Dictionary of land patches.
        edgelist (List[Tuple[int, int]]): List of edges in the graph.
        positions (Dict[int, Tuple[float, float]]): Dictionary of positions for each land patch.
        firefighters (Dict[int, Firefighter]): Dictionary of firefighters on the land.
        __graph_builder (GraphBuilder): Instance of GraphBuilder to build the land graph.
        land_patches, edgelist, positions: graph_builder.build_graph()
    Note: The class properties are private besides edgelist, positions, firefighters which are public.

    Methods:
        spawn_firefighters(self) -> None
        get_colour_maps(self) -> Tuple(Dict,Dict)
        mutate_landpatch(self, landtpatch:Landpatch) -> None
        update_fire_transmission(self, land_patch:Landpatch) -> None
        update(self) -> None:
            - Update firefighters by either:
                - Fighting the fire if they are at a burning treepatch.
                - Setting a destination for a neighboring landpatch.
                - If a firefighter has a new destination then:
                    - Remove references to the old firefighter from their positions.
                    - Insert new references to the firefighters at their positions.
                - Update: Firetransmissions, Tree-growth, Rocks-changing-tree
        get_firefighters(self) -> List[int]
        validate_graph(self, positions:Dict[int,Tuple[float,float]], land_patches:Dict[int,Landpatch]) -> bool:
            - Validates if the graph is connected.
            - vh.edges_planar(self.edgelist) validates whether or not the graph is planar.
            - If the graph cannot be validated, an exception will be raised and the program continues.
    Note: All the class methods are public. """

class Land:
    def __init__(self:Land,
                 configs:Config,
                 land_patches:Dict[int, Landpatch] = {},
                 edgelist:List[Tuple[int, int]] = [],
                 positions:Dict[int, Tuple[float, float]] = {},
                 firefighters:Dict[int, Firefighter] = {}) -> None:
        
        """ Initialize a Land instance.

        Args:
            configs (Config): Configuration settings for the simulation.
            land_patches (Dict[int, Landpatch]): Dictionary of land patches.
            edgelist (List[Tuple[int, int]]): List of edges in the graph.
            positions (Dict[int, Tuple[float, float]]): Dictionary of positions for each land patch.
            firefighters (Dict[int, Firefighter]): Dictionary of firefighters on the land. """
        
        self.__configs = configs
        self.__land_patches = land_patches
        self.edgelist = edgelist
        self.positions = positions
        self.firefighters = firefighters
        self.__graph_builder = GraphBuilder(configs, self.__land_patches)
        self.__land_patches, self.edgelist, self.positions = self.__graph_builder.build_graph()
        
        self.spawn_firefighters()
        
        if not vh.edges_planar(self.edgelist): 
            raise ValueError('Input graph is not planar...')
        if not self.validate_graph(self.positions, self.__land_patches):
            raise RuntimeError('Graph could not be validated...')

    def spawn_firefighters(self) -> None:
        """ Spawn firefighters on the land. """
        firefighters_spawned:int = 0
        while firefighters_spawned < self.__configs['firefighters'][0]:
            spawn_position:int = random.choice(list(self.positions.keys()))
            fireman:Firefighter = Firefighter(firefighters_spawned, self.__configs['firefighters'][1])
            self.firefighters[spawn_position] = fireman
            self.__land_patches[spawn_position].set_firefighter(True)
            firefighters_spawned = firefighters_spawned + 1
    
    def get_colour_maps(self) -> Tuple(Dict,Dict):
        """ Get color maps for landpatches. """
        colour_map:Dict = {}
        no_colour_map:Dict = {}
        for land_patch in self.__land_patches.values():
            if land_patch.get_color() != None:
                colour_map[land_patch.get_patch_id()] = land_patch.get_color()
            else:
                no_colour_map[land_patch.get_patch_id()] = None
        return tuple([colour_map, no_colour_map])
    
    def mutate_landpatch(self, landtpatch:Landpatch) -> None:
        """ Mutate a landpatch. """
        mutated_landpatch = landtpatch.mutate()
        self.__land_patches[mutated_landpatch.get_patch_id()] = mutated_landpatch
    
    def update_fire_transmition(self, land_patch:Landpatch) -> None:
        """ Update fire transmission to neighboring treepatches. """
        neighbors = land_patch.get_neighbors()
        for neighbor in neighbors.values():
            if isinstance(neighbor, Treepatch):
                treepatch:Treepatch = neighbor
                if treepatch.get_lit_state() and random.randint(1, 100) < self.__configs['probabilities'][0]:
                    treepatch.set_lit_state(True)   

    def update(self) -> None:
        """ Update the state of the land for each iteration of the simulation. """
        firefighter_to_move:Dict[int, Firefighter] = {}
        for position in self.firefighters.keys():
            firefighter:Firefighter = self.firefighters[position]
            landpatch:Landpatch = self.__land_patches[position]
            firefighter_should_move = False
            
            if isinstance(self.__land_patches[position], Treepatch):
                treepatch:Treepatch = landpatch
                if treepatch.get_lit_state():
                    firefighter.fight_fire(treepatch)
                else:
                    firefighter_should_move = True
            else:
                firefighter_should_move = True
           
            if firefighter_should_move:
                firefighter_to_move[position] = firefighter
        
        for position in firefighter_to_move.keys():
            firefighter:Firefighter = self.firefighters.pop(position)
            self.__land_patches[position].set_firefighter(False)
            destination = firefighter.move(landpatch, self.get_firefighters())
            self.firefighters[destination] = firefighter
            self.__land_patches[destination].set_firefighter(True)
            
        patches_to_remove:List[int] = []
        for landpatch in self.__land_patches.values():
            if isinstance(landpatch, Treepatch):
                self.update_fire_transmition(landpatch)
            if landpatch.update():
                self.mutate_landpatch(landpatch)

    def get_firefighters(self) -> List[int]:
        """ Get the positions of all firefighters on the land. """
        return list(self.firefighters.keys())

    def validate_graph(self, positions:Dict[int, Tuple[float, float]], land_patches:Dict[int, Landpatch]) -> bool:
        """ Validate the connectivity of the graph. """
        unchecked:list[int] = list(positions.keys())
        validated = []
        while len(unchecked) > 0:
            edge:int = unchecked.pop()
            if edge in validated:
                continue
            for neighbour in land_patches[edge].get_neighbors():
                unchecked.append(neighbour)
            while edge in unchecked:
                unchecked.remove(edge)
            validated.append(edge)
        
        return len(validated) == len(list(positions.keys()))