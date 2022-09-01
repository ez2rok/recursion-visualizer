# AUTOGENERATED! DO NOT EDIT! File to edit: ../02_graph.ipynb.

# %% auto 0
__all__ = ['get_preorder_traversal', 'get_graph_edges', 'get_graph']

# %% ../02_graph.ipynb 4
from .node import Node 

# %% ../02_graph.ipynb 5
import networkx as nx
from typing import List, Dict

# %% ../02_graph.ipynb 6
def get_preorder_traversal(
  history: List[int] # list of node ids recording when each node is first visited and finished being visited
  ) -> List[int]: # preorder traversal of the graph
  """Extract the preorder traversal from `history` by recording the order of
  when each node is first discovered.
  """
  preorder, seen = [], set()
  for id_ in history:
    if id_ not in seen:
        seen.add(id_)
        preorder.append(id_)
  return preorder

# %% ../02_graph.ipynb 7
def get_graph_edges(
  nodes: Dict[int, Node], # map from node id to node
  preorder: List[int], # list of node ids where each node id is recorded when it is first discovered and finished being explored, 
  node_to_edge_labels: Dict[int, str] # map from node id to edge label
  ) -> Dict[tuple, str]: # map from an edge to label (an edge is a tuple of node ids)
  """Convert the preorder traversal `preorder` into a list of edges that define
  the graph of recursive function calls.

  Extract the edges from the preorder traversal by analyzing the depth of
  each node. Collect all the edges and then map each edges to a string label.

  **References:**

  1. Inspired by lee215's
  [solution](https://leetcode.com/problems/recover-a-tree-from-preorder-traversal/discuss/274621/JavaC%2B%2BPython-Iterative-Stack-Solution)
  to *Leetcode 1028. Recover a Tree From Preorder Traversal*.
  """
  
  edge_to_label, stack = {}, []
  for id_ in preorder:
    while len(stack) > nodes[id_].depth:
      stack.pop()
    if stack:
      edge_to_label[(stack[-1], id_)] = node_to_edge_labels[id_]
    stack.append(id_)
  return edge_to_label

# %% ../02_graph.ipynb 8
def get_graph(
    history: List[int], # list of node ids recording when each node is first visited and finished being visited
    nodes: Dict[int, Node], # map from node id to node
    node_to_edge_labels: Dict[tuple, str] # map from a node to an edge label
    ): # a `networkx` graph object
    """Convert the history of recursive function calls, into a `networkx` graph of
    recursive function calls with optionally labeled edges.  
    
    The graph is constructed by 1) extracting the preorder traversal of the
    graph from `history` and then 2) extracting the edges of the graph based on
    the depth of each node in the preorder traversal. 
    """

    # get the preorder traversal; extract the edges of the recursive function call graph
    preorder = get_preorder_traversal(history)
    edges_to_labels = get_graph_edges(nodes, preorder, node_to_edge_labels)

    # create a `networkx` graph object from the edges
    DG = nx.DiGraph()
    DG.add_edges_from(list(edges_to_labels.keys()))
    return DG
