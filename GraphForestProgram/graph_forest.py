from __future__ import annotations
from typing import List, Dict,Tuple
import time
import os
import classes.config_class as cc 
import classes.land_class as lc
import classes.sim_reporting_class as sr
import vis_modules.visualiser_random_forest_graph as vr

""" The Simulation:

    Simulating an area of land composed of various patches with different terrains.
    The adjacency between patches will be represented through a planar graph, i.e., each patch of land will identify a site of a graph and neighboring patches will be those directly connected by a single edge.
    Each patch of land will belong to two main categories (Rock and Tree). The area simulated will hence contain at the initial stage a wood (a collection of tree patches) and some non-flammable areas (rock patches). The area is also populated by a fixed number of firefighters that can move freely on each piece of land.
    The aim of the present project is to describe the evolution of wildfire in this environment.
    The woods have a (small) probability of catching fire (autocombustion) and, once lit, fire can propagate to neighboring tree patches. A tree patch that is devoured by the fire will turn into a rock patch. The rock patches will not propagate fire; however, over time, they have a small probability of turning into a tree patch.
    Run the program to evaluate land geography and evolve the land Tree population over time.

    The simulation configuration:
    Simulate ignition, transmission, and extinction of fires in the forest over n iterations for x randomly generated graphs.

    The simulation configuration steps:
    1: Graph generation: Input (int) number of edges or read graph file 1-6 from cnfg.
    2: Initial landscape pattern: Input (float) tree population percentage (default is 80%).
    3: Probabilities: Input (float, float, float) the 3 probabilities.
    4: Firefighters: Input (int, int) number of firefighters and their skill level (1-100).
    5: Iterations: Input (int) number of simulation iterations / update steps.
    6: Simulation time: Input (float) to define the update speed.
    7: Run simulation: Input (int(7)) to run the simulation and gather data.
    8: Random Forest Fire Simulation Report.
    0: Quit: Input (int(0)) quits the console program.

    Attributes:
        divider (str): A string used for visual separation.
        star_divider (str): A string used for visual separation with stars.
        graph_files (List): List of graph file paths.
        graph_source (int): Source option for graph generation.
        window_title (str): Title for the simulation window.
        sim_reporting (SimReporting): Instance of the SimReporting class for reporting.
        value_errors (int): Count of value errors encountered during configuration.
        runtime_errors (int): Count of runtime errors encountered during configuration.
        graph_menu_key (str): Key for the graph generation menu.
        landscape_menu_key (float): Key for the landscape menu.
        prob_menu_key (Tuple): Key for the probabilities menu.
        firefighters_menu_key (Tuple): Key for the firefighters menu.
        iterations_menu_key (int): Key for the iterations menu.
        time_menu_key (float): Key for the time menu.
        config_settings (Dict): Dictionary containing simulation configuration settings.

    Methods:
        graph_menu(self): Menu for graph generation options.
        landscape_menu(self): Menu for initial landscape pattern options.
        prob_menu(self): Menu for initial probabilities options.
        firefighters_menu(self): Menu for firefighters population and abilities options.
        iterations_menu(self): Menu for number of iteration steps options.
        time_menu(self): Menu for simulation frame update speed options.
        report_menu(self): Menu for reporting options.
        main_menu(self): Main menu for overall configuration settings.
        menu(self): Main menu loop for user interactions.
        start_simulation(self, land: lc.Land): Start the random forest fire simulation. """

class GraphForest:
    def __init__(self:GraphForest,
                 graph_file:str='200',
                 landscape_config:float=80.0,
                 prob_configs:Tuple[float,float,float]=(1.0, 30, 10),
                 firefigther_configs:Tuple[int,int]=(2, 50),
                 iterations_config:int=100,
                 time_config:float=0.01) -> None:
         
        self.divider = '========================================================='
        self.star_divider = '*********************************************************'
        self.graph_files:List = ['cnfg/graph1.dat', 'cnfg/graph2.dat', 'cnfg/graph3.dat', 'cnfg/graph4.dat', 'cnfg/graph5.dat', 'cnfg/graph6.dat']
        self.graph_source:int = 1
        self.window_title:str = 'Random Forest Fire Simulation Graph'
        self.sim_reporting = sr.SimReporting()
        self.value_errors:int = 0
        self.runtime_errors:int = 0
        self.graph_menu_key = graph_file
        self.landscape_menu_key = landscape_config
        self.prob_menu_key = prob_configs
        self.firefighters_menu_key =firefigther_configs
        self.iterations_menu_key = iterations_config
        self.time_menu_key = time_config
        self.config_settings:Dict[str,int,float,Tuple[float,float],Tuple[int,int],int,float] = {'file':self.graph_menu_key,
                                                                                          'graph_source':self.graph_source,
                                                                                          'landscape':self.landscape_menu_key,
                                                                                          'probabilities':self.prob_menu_key,
                                                                                          'firefighters':self.firefighters_menu_key,
                                                                                          'iterations':self.iterations_menu_key,
                                                                                          'time':self.time_menu_key}

    """ Graph Generation:

    Options:
    1: Random: Input (int(1-500)) the number of randomly connected edges.
    2: Read from File: Input (int(1-6)) the location of the text file containing the graph structure.
    
    Standard: Each non-empty line represents an edge, identified by two integers separated by a comma.
    Handling Errors: The GraphReader, GraphBuilder and Land classes are responsible for validating the graph structure.
        Ensure that the generated graph is both connected and planar. """

    def graph_menu(self):
        print(self.divider)
        print('Options: Graph Generation'.upper())
        print(self.divider)
        print('Key 1: Random Generation')
        print('Key 2: Read from File')

        graph_source_input = int(input('\n>> Enter option: ').strip())

        try:
            if graph_source_input < 1 or graph_source_input > 3:
                raise ValueError('Not a valid config key')
            elif graph_source_input == 1:
                self.config_settings['graph_source'] = 1
                print('Random generation has been selected...')
                n_edges_input = int(input('>> Enter number of edges: '))
                if n_edges_input < 4 or n_edges_input > 500:
                    raise ValueError('Number of edges must be between 1-500')
                else:
                    self.graph_menu_key = str(n_edges_input)
                    self.config_settings['file'] = self.graph_menu_key
            elif graph_source_input == 2:
                self.config_settings['graph_source'] = 2
                print('\nGraph Files:')
                key = 0
                for file in self.graph_files:
                    key += 1
                    print(f'> Key {key}: {file}')
                source_input = int(input('\n>> Enter file key (1-6): ').strip())
                if source_input < 1 or source_input > 6:
                    raise ValueError('Not a valid choice for graph generation')
                else:
                    self.graph_menu_key = self.graph_files[source_input-1]
                    self.config_settings['file'] = self.graph_menu_key
        except ValueError as e:
            self.value_errors += 1
            print(f'Error: {e}.')
        finally:
            print(f'Continuing with: {self.graph_menu_key}...')

    """ Initial Landscape Pattern:

    Options:
    1: All Woods: Set up the initial configuration with all patches as tree patches.
    2: All Rocks: Set up the initial configuration with all patches as rock patches.
    3: Random with Fixed Ratio: Choose a fixed ratio (e.g., 80% woods) for a random initial configuration. """

    def landscape_menu(self):
        print(self.divider)
        print('Options: Initial Landscape Pattern'.upper())
        print(self.divider)
        print('Key 1: All Woods')
        print('Key 2: All Rocks')
        print('Key 3: Random with Fixed Ratio')

        initial_landscape_input = int(input('\n>> Enter key (1-3): ').strip())

        try:
            if initial_landscape_input == 1 or initial_landscape_input == 2:
                self.landscape_menu_key = float(initial_landscape_input)
                self.config_settings['landscape'] = self.landscape_menu_key
            elif initial_landscape_input == 3:
                fixed_ratio_input = float(input('>> Enter fixed ratio: '))
                if 1 <= fixed_ratio_input < 100:
                    self.landscape_menu_key = fixed_ratio_input
                    self.config_settings['landscape'] = self.landscape_menu_key
                else:
                    raise ValueError('Ratio must be between 1-99')
            else:
                raise ValueError('Not a valid config key')
        except ValueError as e:
            self.value_errors += 1
            print(f'Error: {e}.')
            print('Please enter a valid option...')
            

    """ Initial Probabilities:
    1: Ignition of fire.
    2: Transmition of fire.
    3: Forest respawn.
    
    Note: All probabilities are intrepreted as percentage float values (0-100). """

    def prob_menu(self):
        print(self.divider)
        print('Options: Initial Probabilities'.upper())
        print(self.divider)
        print('Step 1: Ignition of fire')
        print('Step 2: Transmition')
        print('Step 3: Forest respawn')

        prob_ignition_input = float(input('\n>> 1: Enter probability of ignition of fire (autocombistion): ').strip())
        prob_transmition_input = float(input('>> 2: Enter probability for transmition of fire: ').strip())
        prob_respawn_input = float(input('>> 3: Enter probability of forest respawn: ').strip())

        try:
            if not 0 <= prob_ignition_input <= 100 or not 0 <= prob_transmition_input <= 100 or not 0 <= prob_respawn_input <= 100:
                raise ValueError('All probabilities must be between 0 and 100')
            total_probability = prob_ignition_input + prob_transmition_input + prob_respawn_input
            if total_probability > 100:
                raise ValueError('The sum of probabilities cannot exceed 100')
            self.prob_menu_key = (prob_ignition_input, prob_transmition_input, prob_respawn_input)
        except ValueError as e:
            self.value_errors += 1
            print(f'Error: {e}.')
        finally:
            self.config_settings['probabilities'] = self.prob_menu_key

    """ Firefighters Population and Abilities Options:
    1: Number of Firefighters: Specify the desired number of firefighters in the simulation (1-50).
    2: Average Skill Level: Define the approximate average skill level for firefighters (0-100).

    Note: Individual firefighters may have different skill values. """

    def firefighters_menu(self):
        print(self.divider)
        print('Options: Firefighters Population and Abilities'.upper())
        print(self.divider)
        print('Key 1: Number of Firefighters')
        print('Key 2: Average Skill Level')

        firefighters_population_input = int(input('\n>> Enter number of firefighters: ').strip())
        firefighters_avg_skill_input = int(input('>> Enter firefighters average skill level (min 0 and max 100): ').strip())

        try:
            if not 0 <= firefighters_avg_skill_input <= 100:
                raise ValueError('Average skill level must be between 0 and 100')       
            if not 0 < firefighters_population_input <= 50:
                raise ValueError('Number of firefighters must be between 1 and 50')          
            self.firefighters_menu_key = (firefighters_population_input, firefighters_avg_skill_input)
            self.config_settings['firefighters'] = self.firefighters_menu_key
        except ValueError as e:
            self.value_errors += 1
            print(f'Error: {e}.')

    """ Number of Iteration Steps:
    1: Provide the option to define the number of iteration steps for the simulation. """

    def iterations_menu(self):
        print(self.divider)
        print('Options: Number of Iteration Steps'.upper())
        print(self.divider)

        self.iterations_menu_key = int(input('\n>> Enter number of iterations: ').strip())

        try:
            if not 1 <= self.iterations_menu_key <= 1000:
                self.iterations_menu_key = int(100)
                raise ValueError('Iterations must be between 1 and 1000') 
            else:
                self.config_settings['iterations'] = self.iterations_menu_key
        except ValueError as e:
            self.value_errors += 1
            print(f'Error: {e}.')
        finally:
            self.config_settings['iterations'] = self.iterations_menu_key
            print(f'Continueing with: {self.iterations_menu_key}...')

    """ Time limit for the simulation:
    1: Update Speed. """

    def time_menu(self):
        print(self.divider)
        print('Options: Simulation Frame Update Speed'.upper())
        print(self.divider)

        self.time_menu_key = float(input('\n>> Enter frame update speed as a floating point number: ').strip())

        try:
            if not 0.001 <= self.time_menu_key <= 10:
                self.time_menu_key = float(0.01)
                raise ValueError('Iterations must be between 0.001 and 10') 
            else:
                self.time_menu_key = self.time_menu_key
        except ValueError as e:
            self.value_errors += 1
            print(f'Error: {e}.')
        finally:
            self.config_settings['time'] = self.time_menu_key
            print(f'Continueing with: {self.time_menu_key}...')

    """ Simulation Reporting:

    1: Simulation Graph from the project description (sim_graph_1.png).
    2: Population Mean (unfinished) Graph (sim_statistics_1.png).
    3: Open the generated pdf report generic_sim_graph_1.pdf in a browser window.
    4: Show exceptions raised while configuring the simulation parameters. """

    def report_menu(self):
        print(self.divider)
        print('Options: Reporting'.upper())
        print(self.divider)
        print('Key 1: Show Simulation Graph')
        print('Key 2: Show Population Mean')
        print('Key 3: Open PDF Report in browser')
        print('Key 4: Show Raised Exceptions')

        report_menu_key = int(input('\n>> Enter reporting option: ').strip())

        try:
            if report_menu_key < 1 or report_menu_key > 4:
                raise ValueError('Invalid config key')
            elif report_menu_key == 1:
                self.sim_reporting.read_jpg('sim_graph_1.jpg')
            elif report_menu_key == 2:
                self.sim_reporting.read_jpg('sim_statistics_1.jpg')
            elif report_menu_key == 3:
                os.startfile('generic_graph_1.pdf')
            elif report_menu_key == 4:
                print(f'\n{self.star_divider}')
                print(f'Exceptions raised while configuring:\n> ValueErrors: {self.value_errors}\n> RunTimeErrors: {self.runtime_errors}\n> Errors Total: {self.value_errors+self.runtime_errors}')
                print(f'{self.star_divider}\n')
        except ValueError as e:
            self.value_errors += 1
            print(f'Error: {e}.')

    """ Set up parameters for random graph generation and simulation settings:

    Configurations and Options:
    1: Define the parameters for random graph generation: number of edges or file source.
    2: Initial tree population percentage.
    3: Probabilities for ignition, transmission, and forest respawn.
    4: Number of firefighters.
    5: Number of iterations.
    6: Time limit for simulation - update speed.
    7: Run the simulation and generate report data.
    8: Access simulation reporting details.
    0: Quit the console program. """

    def main_menu(self):
        print(self.divider)
        print('Random Forest Fire Simulation Configurations'.upper())
        print(self.divider)
        print('Key 1: \tGraph Generation (' + str(self.graph_menu_key) + ')')
        print('Key 2: \tInitial Landscape Pattern (' + str(self.landscape_menu_key) + ')')
        print('key 3: \tInitial Probabilities (' + str(self.prob_menu_key) + ')')
        print('Key 4: \tFirefighters Population and Abilities (' + str(self.firefighters_menu_key) + ')')
        print('Key 5: \tNumber of Iteration Steps (' + str(self.iterations_menu_key) + ')')
        print('Key 6: \tSimulation Time (update speed) (' + str(self.time_menu_key) + ')')
        print('Key 7: \tStart Random Forest Fire Simulation')
        print('Key 8: \tSimulatation Reporting')
        print('Key 0: \tQuit Simulatation Program')

        self.main_config_key = int(input('\n>> Enter key 1 to 8 (or 0 to quit): ').strip())

    def menu(self):
        while True:
            self.main_menu() 
            if self.main_config_key == 1:
                self.graph_menu()       
            elif self.main_config_key == 2:
                self.landscape_menu()
            elif self.main_config_key == 3:
                self.prob_menu()
            elif self.main_config_key == 4:
                self.firefighters_menu()
            elif self.main_config_key == 5:
                self.iterations_menu()
            elif self.main_config_key == 6:
                self.time_menu()
            elif self.main_config_key == 7:
                cc.Config(self.config_settings)
                try:
                    land = lc.Land(self.config_settings)
                    print('\nStarting random forest fire simulation...')
                    print(f'Simulation configurations: {cc.Config.get_configs(self)}')
                    self.start_simulation(land)
                    print('\nRandom forest fire simulation has ended...')
                except ValueError as e:
                    self.value_errors += 1
                    print(f'Error: {e}.')
                except RuntimeError as e:
                    self.runtime_errors += 1
                    print(f'Error: {e}.')
            elif self.main_config_key == 8:
                self.report_menu()
            elif self.main_config_key == 0:
                print(self.star_divider)
                print('Random forest fire simulation program is quitting...')
                print(self.star_divider)
                break
            else:
                self.value_errors += 1
                print(ValueError(f'Error: {self.main_config_key} is not a valid key...'))
                print('Please enter a new config key (0-8)')
    
    def start_simulation(self, land:lc.Land):
        """ Start the simulation and update with  initial parameters. """
        colour_map, no_colour_map = land.get_colour_maps()
        """ Assigning an instance of the Visualiser object with the parameters and data structures defnied by the class to the variable vis. """
        vis = vr.Visualiser(edges=land.edgelist, Colour_map=colour_map, pos_nodes=land.positions, node_size=50, vis_labels=True, window_title=self.window_title)
        vis.update_node_colours(colour_map)
        firefighter:List[int] = land.get_firefighters()
        vis.update_node_edges(firefighter)
        completed_updates = 0
        rock_population = len(list(no_colour_map.values()))
        tree_population = list(colour_map.values()).count(256)
        wildfires = len(colour_map) - rock_population - tree_population
        self.sim_reporting.update_sim_data(trees=tree_population, rocks=rock_population, wildfire=wildfires)

        while completed_updates < self.config_settings['iterations']:
            """ The Land update method to update the state of the land. """
            land.update()
            colour_map, no_colour_map = land.get_colour_maps()
            rock_population = len(list(no_colour_map.values()))
            tree_population = list(colour_map.values()).count(256)
            wildfires = len(colour_map) - rock_population - tree_population
            self.sim_reporting.update_sim_data(trees=tree_population, rocks=rock_population, wildfire=wildfires)
            vis.update_node_colours(colour_map)
            firefighter = land.get_firefighters()
            vis.update_node_edges(firefighter)
            completed_updates = completed_updates + 1
            time.sleep(self.config_settings['time'])
        while vis.is_open():
            time.sleep(2.2)
            vis.close()
            """ Call SimReporting methods """
            self.sim_reporting.generate_plots()
            self.sim_reporting.genrate_report_pdf()
            print('Generating report...')
            print('Report generated and saved to: generic_graph_1.pdf.') 
        


if __name__ == '__main__':
    GraphForest().menu()
