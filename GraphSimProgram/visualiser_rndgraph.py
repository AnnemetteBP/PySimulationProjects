"""
This module provides Visualiser, a class for displaying the status of a collection of edges and sites forming the graph of a simulation.

Requirements
------------
Package matplotlib https://matplotlib.org/ which can be installed via PIP.
Package networkx https://networkx.org/ which can be installed via PIP.
Python 3.7 or higher.



Notes
-----
This module provided as material for the phase 1 project for DM857, DS830 (2023). 
"""

from __future__ import annotations # to use a class in type hints of its members
from typing import List, Optional, Dict
import matplotlib.pyplot as plt
import networkx as nx
import random

class Visualiser:
  """Each instance of this class maintains a window where it displays the status of a given collection of edges and sites forming the graph of a simulation."""

  def __init__(self:Visualiser, 
               edges:List[(int,int)],
               val_map: Optional[Dict[int:float]]={},
               def_col: Optional[float] = 0.,
               node_size : Optional[int] = 500,
               vis_labels: Optional[bool] = False,
               window_title : Optional[str]=None)->None:
    """
    Parameters
    ----------
    edges: List[(int,int)]
      List containing the edges (Tuples of 2 vertices) forming the 2D surface for the simulation.
    val_map: Dict[int:float]
      Dictionary containing the color of each vertex (expressed as a float)
    def_col:
      Color of the vertices not reported in val_map
    node_size: int, default 500
      Control the size of the drawn nodes
    window_title : Optional[str], default = None
      The title of the window.
    """
    self._edges = edges
    self._values = [val_map.get(i,def_col) for i in set().union(*edges)]
    self._def_col = def_col
    self._vis_labels = vis_labels
    self._H = nx.Graph(self._edges)  # create a Graph dict mapping nodes to nbrs
    self._values = [val_map.get(i,def_col) for i in self._H]

    # Need to create a layout when doing
    # separate calls to draw nodes and edges
    self._pos = nx.spring_layout(self._H,k=2)

    fig, ax = plt.subplots()
    # title
    if not window_title:
      window_title = 'CellSim Visualiser'
    fig.canvas.manager.set_window_title(window_title)    
    # listen to close events
    self._is_open = True
    def on_close(_)->None:
      self._is_open = False
    fig.canvas.mpl_connect('close_event', on_close )
  
    nx.draw_networkx_nodes(self._H, self._pos,
                       node_color = self._values, node_size = 500)
    
    
    nx.draw_networkx_edges(self._H, self._pos, arrows=False)
    if(self._vis_labels):
      nx.draw_networkx_labels(self._H, self._pos)

    # make sure our window is on the screen and drawn
    plt.show(block=False)
    plt.pause(1.1)
  
  def is_open(self:Visualiser) -> bool:
    """
    Whether the window managed by the visualiser is open or not.
    """
    return self._is_open

  def close(self:Visualiser) -> None:
    """Closes the window destroying this visualiser."""
    plt.close()

  def wait_close(self:Visualiser):
    """
    Suspends the current execution until the visualiser window is manually closed by the user.
    """
    plt.show()


  def update(self:Visualiser,val_map:Dict[int:float]) -> None:
    """Informs this visualiser that the status of its colours has been updated."""
    if self.is_open() :
      self._values = [val_map.get(i,self._def_col) for i in self._H]
      
      nx.draw_networkx_nodes(self._H, self._pos,
                       node_color = self._values, node_size = 500)
      nx.draw_networkx_edges(self._H, self._pos, arrows=False)
      plt.pause(1.1)
