from __future__ import annotations
from typing import List, Dict
import os
import random
import matplotlib.pyplot as plt
from models import Vertex
    
class Graph():
    """
    A class representing a graph for simulation.
    Only modules part of the Python standard libraray (https://docs.python.org/3/library/index.html) and matplotlib.
    Uses the models module / vertex model.

    Attributes:
        edges (List[(int, int)]): List of edges in the graph.
        graph_file_path (str): Path to the graph file.
        colour_key (int): Initial coloring pattern configuration.
        procedure_key (int): Update procedure configuration.
        ordered_metrics (List[float]): Metrics for the ordered update procedure.
        max_violation_metrics (List[float]): Metrics for the max violation update procedure.
        monte_carlo_metrics (List[float]): Metrics for the Monte Carlo update procedure.
        vertecies (Dict[str, Vertex]): Dictionary of vertices in the graph.
        val_map (Dict[int, float]): Mapping of vertex to color.

    Methods:
        initialize_vertecies(): Initialize the vertices of the graph.
        read_graph_from_file(): Read the graph from a file.
        generate_random_graph(n_edges: int) -> List[(int, int)]: Generate a random graph.
        set_initial_coloring_pattern() -> Dict[int: float]: Set the initial coloring pattern.
        run_update_procedure() -> Dict[int: float]: Run the selected update procedure.
        update_ordered() -> Dict[int: float]: Update the graph using the ordered procedure.
        update_max_violation() -> Dict[int: float]: Update the graph using the max violation procedure.
        update_monte_carlo() -> Dict[int: float]: Update the graph using the Monte Carlo procedure.
        local_metric(vertex_name: str) -> float: Calculate the local metric for a vertex over the entire graph.
        global_metric() -> float: Calculate the frustration product of the global metric for the entire graph.
        validate_graph() -> bool: Validate the graph structure.
    """
    def __init__(self:Graph, graph_file_path:str, colour_key:int, procedure_key:int) -> None:
        """
        Initialize the Graph object.

        Examples:
        >>> graph = Graph("graph.txt", 1, 2)
        """
        self.edges = []
        self.graph_file_path = graph_file_path
        self.colour_key = colour_key
        self.procedure_key = procedure_key
        self.ordered_metrics = []
        self.max_violation_metrics = []
        self.monte_carlo_metrics = []

        if len(self.graph_file_path) > 0 :
            self.edges = self.read_graph_from_file()
            assert self.edges is not None, AssertionError('Error: File not found.')
        else:
            n_edges = int(input('Enter number of graph edges: ').strip())
            self.edges =  self.generate_random_graph(n_edges)

        self.val_map = self.set_initial_coloring_pattern()
        self.initialize_vertecies()

        assert self.validate_graph(), AssertionError('Graph Validation Error: Program is quitting...')

    def initialize_vertecies(self:Graph) -> None:
        """
        Initialize the vertices of the graph.

        Examples:
        >>> graph = Graph("graph.txt", 1, 2)
        >>> graph.initialize_vertecies()
        """
        self.vertecies = {}

        for edge in self.edges:
            if not str(edge[0]) in self.vertecies:
                vertex0 = Vertex(str(edge[0]))
                self.vertecies[vertex0.name] = vertex0
            else:
                vertex0 = self.vertecies[str(edge[0])]

            if not str(edge[1]) in self.vertecies:
                vertex1 = Vertex(str(edge[1]))
                self.vertecies[vertex1.name] = vertex1
            else:
                vertex1 = self.vertecies[str(edge[1])]
            
            vertex0.neighbours.append(vertex1.name)
            vertex1.neighbours.append(vertex0.name)

        for vertex in self.vertecies:
            self.vertecies[vertex].color = self.val_map[int(vertex)]

    def read_graph_from_file(self:Graph) -> List[(int, int)]:
        """
        Read the graph from a file. If an exception is raised, use default parameters.

        Examples:
        >>> graph = Graph("graph_cnfg/graph2.dat", 1, 2)
        >>> edges = graph.read_graph_from_file()
        """
        try:
            if not os.path.exists(self.graph_file_path):
                self.graph_file_path = 'graph_cnfg/graph2.dat'
                print(f'The file path is invalid...\nContinuing simulation with graph file: {self.graph_file_path}.')

            file = open(self.graph_file_path, 'r', encoding='utf-8')
            lines = file.readlines()
            edges = []

            for line_number, line in enumerate(lines, start=1):
                line_text = line.strip()

                if line_text.startswith('#'):
                    continue
                elif not line_text:
                    continue
                elif ',' not in line_text:
                    continue

                site0, site1 = map(str.strip, line_text.split(','))

                if site0 and site1:
                    edges.append((int(site0), int(site1)))
                else:
                    raise ValueError(f'Value Error at line {line_number}.')

        except ValueError as e:
            print(f'Error: {e}.')
        finally:
            file.close()
            return edges

    def generate_random_graph(self:Graph, n_edges:int) -> List[(int, int)]:
        """
        Generate a random graph.

        Examples:
        >>> graph = Graph("", 1, 2)
        >>> random_edges = graph.generate_random_graph(10)
        """
        edges = []
        site0 = random.randint(0, n_edges)
        items_count = n_edges
        
        while items_count >= 0 :
            site1 = random.randint(0, n_edges)
            while site0 == site1 :
                site1 = random.randint(0, n_edges)
            item = (site0, site1)
            edges.append(item)
            site0 = site1
            items_count = items_count - 1
        
        return edges

    def set_initial_coloring_pattern(self:Graph) -> Dict[int:float]:
        """
        Set the initial coloring pattern.

        Examples:
        >>> graph = Graph("", 1, 2)
        >>> initial_colors = graph.set_initial_coloring_pattern()
        """ 
        colors = {}
        
        for edge in self.edges:
            if self.colour_key == 1:
                colors[int(edge[0])] = float(0)
                colors[int(edge[1])] = float(0)
            elif self.colour_key == 2:
                colors[int(edge[0])] = float(1)
                colors[int(edge[1])] = float(1)
            else:
                colors[int(edge[0])] = float(random.randint(0, 1))
                colors[int(edge[1])] = float(random.randint(0, 1))
        
        return colors

    def run_update_procedure(self:Graph) -> Dict[float:int]:
        """
        Run the selected update procedure.

        Examples:
        >>> graph = Graph("graph.txt", 1, 2)
        >>> updated_colors = graph.run_update_procedure()
        """ 
        self.frustration_metric = self.global_metric()
        if self.procedure_key == 1:
            self.ordered_metrics.append(self.frustration_metric)
            return self.update_ordered()
        elif self.procedure_key == 2:
            self.max_violation_metrics.append(self.frustration_metric)
            return self.update_max_violation()
        else:
            self.monte_carlo_metrics.append(self.frustration_metric)
            return self.update_monte_carlo()

    def update_ordered(self:Graph) -> Dict[int:float]:
        """
        Update the graph using the ordered procedure.

        Examples:
        >>> graph = Graph("graph.txt", 1, 2)
        >>> updated_colors = graph.update_ordered()
        """
        for vertex in self.vertecies.values():
            local_action = self.local_metric(vertex.name)
            if local_action > 0:
                vertex.color = int(not bool(vertex.color))
                self.val_map[int(vertex.name)] = vertex.color
        
        return self.val_map

    def update_max_violation(self:Graph) -> Dict[int:float]:
        """
        Update the graph using the max violation procedure.

        Examples:
        >>> graph = Graph("graph.txt", 1, 2)
        >>> updated_colors = graph.update_max_violation()
        """
        max_localaction = 0.0
        max_vertex = None

        for vertex in self.vertecies.values():
            if max_localaction < self.local_metric(vertex.name):
                max_localaction = self.local_metric(vertex.name)
                max_vertex = vertex

        if max_vertex != None:
            max_vertex.color = int(not bool(max_vertex.color))
            self.val_map[int(max_vertex.name)] = max_vertex.color
        
        return self.val_map
   
    def update_monte_carlo(self:Graph) -> Dict[int:float]:
        """
        Update the graph using the Monte Carlo procedure.

        Examples:
        >>> graph = Graph("graph.txt", 1, 2)
        >>> updated_colors = graph.update_monte_carlo()
        """
        for vertex in self.vertecies.values():
            local_action = self.local_metric(vertex.name)
            if (local_action * local_action) > random.randint(0,1):
                vertex.color = int(not bool(vertex.color))
                self.val_map[int(vertex.name)] = vertex.color
        
        return self.val_map

    def local_metric(self: Graph, vertex_name:str) -> float:
        """
        Calculate the local metric for a vertex over the entrie graph.

        Examples:
        >>> graph = Graph("graph.txt", 1, 2)
        >>> local_metric_value = graph.local_metric("1")
        """ 
        local_vertex:Vertex = self.vertecies[vertex_name]
        result = 0.0
        local_val = 1 - 2 * local_vertex.color

        for neighbour in local_vertex.neighbours:
            neighbour_vertex = self.vertecies[neighbour]
            neighbour_val = local_val * (1 - 2 * neighbour_vertex.color)
            result = result + neighbour_val
        
        return result       

    def global_metric(self: Graph) -> float:
        """
        Calculate the product of the frustration as a global metric for the entire graph.

        Examples:
        >>> graph = Graph("graph.txt", 1, 2)
        >>> global_metric_value = graph.global_metric()
        """ 
        result = 0

        for vertex in self.vertecies:
            result = result + self.local_metric(vertex)
        
        return 0.5 * result

    def validate_graph(self:Graph) -> bool:
        """
        Validate the graph structure.

        Examples:
        >>> graph = Graph("graph.txt", 1, 2)
        >>> is_valid = graph.validate_graph()
        """ 
        searching = []
        done = []
        searching.append(self.edges[0][0])

        while len(searching) > 0:
            subject = str(searching.pop())
            while subject in searching:
                searching.remove(subject)
            if subject in done:
                continue
            for neighbour in self.vertecies[subject].neighbours:
                searching.append(neighbour)
            while subject in searching:
                searching.remove(subject)
            done.append(subject)
        
        return len(done) == len(self.vertecies)
