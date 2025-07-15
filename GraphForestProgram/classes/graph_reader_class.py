from typing import List, Dict, Tuple
import random

""" The Graph Reader Class:

    Reads a graph from the config directory containing 6 .dat extension files used to generate the randomly connected land graph.

    Attributes:
        edgeslist (List[Tuple[int, int]]): List of edges in the graph.
        positions (Dict[int, Tuple[float, float]]): Dictionary of positions for each land patch.
        graph_lines (List[str]): List of lines read from the graph file.
    Note: All class properties are public.

    Methods:
        read_graph(self, filepath: str) -> Tuple[List[Tuple[int, int]], Dict[int, Tuple[float, float]]]
    Note: The class method is public. """

class GraphReader:
    
    def read_graph(self, filepath:str) -> Tuple[List[Tuple[int, int]], Dict[int, Tuple[float, float]]]:
        edgeslist:List[Tuple[int, int]] = []
        positions:Dict[int,Tuple[float,float]] = {}
        graph_lines:list[str] = []

        with open(filepath) as graph_file:
            graph_lines = graph_file.readlines()
        
        edge_index:int = 0
        
        for graph_line in graph_lines:
            patches_str = graph_line.split(',')
            
            if len(patches_str) == 2:
                if str.isdigit(patches_str[0].strip()) and str.isdigit(patches_str[1].strip()):
                    patch_a:int = patches_str[0].strip()
                    patch_b:int = patches_str[1].strip()
                    edgeslist.insert(edge_index, tuple([int(patch_a), int(patch_b)]))                   
                    positions[int(patch_a)] = tuple([random.uniform(0.0, 10.0), random.uniform(0.0, 10.0)])
                    positions[int(patch_b)] = tuple([random.uniform(0.0, 10.0), random.uniform(0.0, 10.0)])
                    edge_index = edge_index + 1
                
                else:
                    print(ValueError('Graph file has syntax errors...'))
        
        return tuple([edgeslist, positions])