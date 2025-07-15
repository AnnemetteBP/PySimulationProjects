from __future__ import annotations
from typing import Dict, Tuple

""" The Config Class:

    Utilized by the forest_graph module to manage simulation configurations.

    Attributes:
        config_settings (Dict): A dictionary containing simulation configuration settings.
        graph_file (str): The file used for the simulation graph.
        graph_source (str): The source of the simulation graph.
        landscape_config (float): Percentage of landpatches populated by trees
        prob_configs (Tuple[float, float, float]): Probabilities in percentage for ignition of fire, transmition, forest respawm.
        firefigther_configs (Tuple[int, int]): Number of firefighters and skill-level.
        iterations_config (int): Configuration for the number of update iterations.
        time_config (float): Configuration for the simulation update speed.
    Note: All properties are public.

    Methods:
        __init__(self, config_settings: Dict[str, int, float, Tuple[float, float, float], Tuple[int, int], int, float]) -> None:
            Initializes the Config instance with the provided configuration settings.

        get_configs(self) -> Dict:
            Returns the current configuration settings.

        set_configs(self, configs: Dict[str, int, float, Tuple[float, float, float], Tuple[int, int], int, float]) -> None:
            Sets the configuration settings based on the provided dictionary.
        Note: All methods are public. """

class Config:
    def __init__(self:Config,
                 config_settings:Dict[str, int, float, Tuple[float, float, float], Tuple[int, int], int, float]) -> None:
        
        self.config_settings = config_settings
        self.graph_file = self.config_settings.get('file')
        self.graph_source = self.config_settings.get('graph_source')
        self.landscape_config = self.config_settings.get('landscape')
        self.prob_configs = self.config_settings.get('probabilities')
        self.firefigther_configs = self.config_settings.get('firefigthers')
        self.iterations_connfig = self.config_settings.get('iterations')
        self.time_config = self.config_settings.get('time')

    def get_configs(self) -> Dict:
        """ Return the current configuration settings.

        Returns:
            Dict: The current configuration settings. """       
        return self.config_settings

    def set_configs(self, configs:Dict[str, int, float, Tuple[float, float, float], Tuple[int, int], int, float]) -> None:
        """ Set the configuration settings based on the provided dictionary.
        
        Args:
            configs (Dict): A dictionary containing simulation configuration settings. """        
        self.config_settings = configs