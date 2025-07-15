from __future__ import annotations
from typing import List, Dict,Tuple
import vis_modules.graph_helper as vh
from classes.graph_reader_class import GraphReader
from classes.landpatch_base_class import Landpatch
from classes.rockpatch_sub_class import Rockpatch
from classes.treepatch_sub_class import Treepatch

""" The GraphBuilder Class:

    Builds a graph based on inputs.
    Utilized by the land module.

    Attributes:
        land_patches (Dict[int, Landpatch]): Dictionary of land patches.
        configs (any): Configuration settings for building the graph.
        number_of_rocks (int): Number of rock patches in the graph.
        number_of_trees (int): Number of tree patches in the graph.
    Note: All class properties are public.

    Methods:
        build_graph(self) -> Tuple[Dict[int, Landpatch], List[Tuple[int, int]], Dict[int, Tuple[float, float]]]
        create_landpatches(self, edgelist: List[Tuple[int, int]], positions: Dict[int, Tuple[float, float]]) -> None
        create_landpatch(self, patch_id: int, pos: Tuple[float, float]) -> None
    Note: All the class methods are public. """

class GraphBuilder:
    def __init__(self:GraphBuilder,
                 configs,
                 land_patches) -> None:
        
        """ Initialize a GraphBuilder instance.

        Args:
            configs (any): Configuration settings for building the graph.
            land_patches (Dict[int, Landpatch]): Dictionary of land patches. """
        
        self.land_patches:Dict[int, Landpatch] = land_patches
        self.configs = configs
        self.number_of_rocks = 0
        self.number_of_trees = 0

    def build_graph(self) -> Tuple[Dict[int, Landpatch], List[Tuple[int, int]], Dict[int, Tuple[float, float]]]:
        """ Build the graph based on the specified configuration.

        Returns:
            Tuple[Dict[int, Landpatch], List[Tuple[int, int]], Dict[int, Tuple[float, float]]]: Tuple containing
            land_patches, edgelist, and positions. """
        
        if self.configs['graph_source'] == 1:
            self.edgelist, self.positions = vh.voronoi_to_edges(int(self.configs['file']))
            self.create_landpatches(self.edgelist, self.positions)
        elif self.configs['graph_source'] == 2:
            graph_reader = GraphReader()
            self.edgelist, self.positions = graph_reader.read_graph(self.configs['file'])
            self.create_landpatches(self.edgelist, self.positions)
        else:
            print(ValueError('Selected graph source is invalid...'))
        
        return tuple([self.land_patches, self.edgelist, self.positions])

    def create_landpatches(self, edgelist:List[Tuple[int, int]], positions:Dict[int, Tuple[float, float]]) -> None:
        """ Create land patches based on the given edgelist and positions.

        Args:
            edgelist (List[Tuple[int, int]]): List of edges in the graph.
            positions (Dict[int, Tuple[float, float]]): Dictionary of positions for each land patch. """
        for patch_id in positions.keys():
            self.create_landpatch(patch_id, positions[patch_id])
        for neighbors in edgelist:
            first_patch = self.land_patches[int(neighbors[0])]
            second_patch = self.land_patches[int(neighbors[1])]
            first_patch.add_landpatch_to_neighbour(second_patch)
            second_patch.add_landpatch_to_neighbour(first_patch)

    def create_landpatch(self, patch_id:int, pos:Tuple[float, float]) ->  None:
        """ Create a land patch based on the given patch_id and position.

        Args:
            patch_id (int): Identifier for the land patch.
            pos (Tuple[float, float]): Position of the land patch. """
        target_percentage_of_trees = self.configs['landscape'] / 100
        if len(self.land_patches) > 0:
            current_tree_percentage = self.number_of_trees / len(self.land_patches)
        else:
            current_tree_percentage = 0
        if current_tree_percentage < target_percentage_of_trees:
            land_patch = Treepatch(patch_id, {}, False, self.configs['probabilities'][0])
            self.number_of_trees = self.number_of_trees + 1
        else:
            land_patch  = Rockpatch(patch_id, {}, self.configs['probabilities'][2])
            self.number_of_rocks = self.number_of_rocks + 1
        land_patch.set_position(pos)
        self.land_patches[land_patch.get_patch_id()] = land_patch