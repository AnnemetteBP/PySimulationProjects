from __future__ import annotations
import time
from matplotlib import pyplot as plt
import visualiser_rndgraph as vr
import graph_class as gc
import os

class GraphSim():
    """
    A class for simulating random graph configurations.
    Only modules part of the Python standard libraray (https://docs.python.org/3/library/index.html).
    Uses the visualiser_rndgraph and graph_class modules.

    Attributes:
        graph_config_key (str): File path for graph configuration.
        colour_config_key (int): Initial colouring pattern configuration.
        procedure_config_key (int): Update procedure configuration.
        iterations_config_key (int): Number of simulation updates.
        speed_config_key (float): Simulation update speed.
        frustration_metrics (dict): Measured global metric

    Methods:
        graph_menu(): Select graph generation configuration.
        coloring_menu(): Select initial colouring pattern configuration.
        update_procedure(): Select update procedure configuration.
        simulation_iterations(): Set the number of simulation updates.
        simulation_speed(): Set the simulation update speed.
        main_menu(): Display the main simulation menu.
        menu(): Run the simulation menu loop.
        run_simulation(): Execute the graph simulation.
        graph_sim_report(): Generate report / plot of the graph frustration. 
    """
    def __init__(self:GraphSim) -> None:
        """
        Initialize the GraphSim object with default configurations.
        """
        self.graph_config_key = 'graph_cnfg/graph2.dat'
        self.colour_config_key = 3
        self.procedure_config_key = 1
        self.iterations_config_key = 10
        self.speed_config_key = 0.01
        self.frustration_metrics = {}

    def graph_menu(self:GraphSim) -> None:
        """
        Select graph generation configuration.

        Examples:
        >>> sim = GraphSim()
        >>> sim.graph_menu()  # User input required
        """
        print('Select graph generation config:')
        print('Read graph from file: \tEnter file path')
        print('Generate random graph: \tLeave empty')
        self.graph_config_key = input('''Enter file path: ''').strip()  

    def coloring_menu(self:GraphSim) -> None:
        """
        Select initial colouring pattern configuration.

        Examples:
        >>> sim = GraphSim()
        >>> sim.coloring_menu()  # User input required
        """
        print('Select initial colouring pattern config:')
        print('All 0: \t1')
        print('All 1: \t2')
        print('Random: 3')
        self.colour_config_key = int(input('''Enter choice 1 to 3: ''').strip())

    def update_procedure(self:GraphSim) -> None:
        """
        Select update procedure configuration.

        Examples:
        >>> sim = GraphSim()
        >>> sim.update_procedure()  # User input required
        """
        print('Select update procedure config:')
        print('Ordered: \t1')
        print('MaxViolation: \t2')
        print('MonteCarlo: \t3')
        self.procedure_config_key = int(input('''Enter choice 1 to 3: ''').strip())

    def simulation_iterations(self:GraphSim) -> None:
        """
        Set the number of simulation updates.

        Examples:
        >>> sim = GraphSim()
        >>> sim.simulation_iterations()  # User input required
        """
        print('Select number of simulation updates:')
        self.iterations_config_key = int(input('''Enter iterations: ''').strip())

    def simulation_speed(self:GraphSim) -> None:
        """
        Set the simulation update speed.

        Examples:
        >>> sim = GraphSim()
        >>> sim.simulation_speed()  # User input required
        """
        print('Select simulation update speed:')
        self.speed_config_key = float(input('''Enter a floating point number: ''').strip())

    def main_menu(self:GraphSim) -> None:
        """
        Display the main simulation menu.

        Examples:
        >>> sim = GraphSim()
        >>> sim.main_menu()  # User input required
        """
        print('Random Graph Simulation Configurations:')
        print('1: \tGraph Generation (' + self.graph_config_key + ')')
        print('2: \tInitial Colouring Pattern (' + str(self.colour_config_key) + ')')
        print('3: \tUpdate Procedure (' + str(self.procedure_config_key) + ')')
        print('4: \tSet Simulation Iterations (' + str(self.iterations_config_key) + ')')
        print('5: \tSet Simulation Speed (' + str(self.speed_config_key) + ')')
        print('6: \tStart Simulation')
        print(print('7: \tShow Simulatation Report'))
        
        self.main_config_key = input('Enter choice 1 to 7: ').strip()
        
        assert int(self.main_config_key) >= 0 and int(self.main_config_key) <= 7, AssertionError('Not a valid config key...')

    def menu(self:GraphSim) -> None:
        """
        Run the simulation menu loop.

        Examples:
        >>> sim = GraphSim()
        >>> sim.menu()  # User input required
        """
        while True:
            self.main_menu()
            if self.main_config_key == '1':
                self.graph_menu()       
            elif self.main_config_key == '2':
                self.coloring_menu()
            elif self.main_config_key == '3':
                self.update_procedure()
            elif self.main_config_key == '4':
                self.simulation_iterations()
            elif self.main_config_key == '5':
                self.simulation_speed()
            elif self.main_config_key == '6':
                self.graph = gc.Graph(self.graph_config_key, self.colour_config_key, self.procedure_config_key)
                print('Starting simulation...')
                self.run_simulation()
                print('Simulation has ended...')
            elif self.main_config_key == '7':
                self.graph_sim_report()
            elif self.main_config_key == '0':
                print('Program is quitting...')
                break 
    
    def run_simulation(self:GraphSim) -> None:
        """
        Execute the graph simulation.

        Examples:
        >>> sim = GraphSim()
        >>> sim.run_simulation()  # Simulation execution (no user input)
        """
        visualizer = vr.Visualiser(self.graph.edges, self.graph.val_map)
        counter = self.iterations_config_key

        while counter > 0:
            new_val_map = self.graph.run_update_procedure()
            visualizer.update(new_val_map)
            counter = counter - 1
            time.sleep(self.speed_config_key)
        visualizer.close()
    
    def graph_sim_report(self:GraphSim) -> None:
        """
        Generate a simulation report of the graph frustration over n update steps and x procedure.

        Examples:
        >>> graph = Graph("graph.txt", 1, 2)
        >>> graph.graph_sim_report()
        """
        if len(self.graph.ordered_metrics) > 0:
            self.frustration_metrics['Ordered'] = self.graph.ordered_metrics
        elif len(self.graph.max_violation_metrics) > 0:
            self.frustration_metrics['MaxViolation'] = self.graph.max_violation_metrics
        elif len(self.graph.monte_carlo_metrics) > 0:
            self.frustration_metrics['MonteCarlo'] = self.graph.monte_carlo_metrics

        for key, values in self.frustration_metrics.items():
            plt.plot(values, label=key)
        
        plt.xlabel('Number of update steps')
        plt.ylabel('Frustration of the graph')
        plt.title('Graph Simulation Report')
        plt.legend()
        plt.grid()

        plt.show() 

if __name__ == '__main__':
    #import doctest
    #doctest.testmod()
    GraphSim().menu()
