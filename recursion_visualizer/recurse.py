# AUTOGENERATED! DO NOT EDIT! File to edit: ../01_recurse.ipynb.

# %% auto 0
__all__ = ['RecursionVisualizer']

# %% ../01_recurse.ipynb 3
from .node import Node 
from .graph import get_graph

# %% ../01_recurse.ipynb 5
class RecursionVisualizer:
  """A class that provides a decorator for visualizing recursion trees and caching results."""

  def __init__(self,
               verbose: bool = False, # if true, print all nodes
               animate: bool = True, # if true, create an animation of the recursion tree
               save: bool = False, # if true, save the animation to a html file
               path: str ='', # path to save the animation to
               ): 
    
    self.verbose = verbose
    self.animate = animate
    self.save = save
    self.path = path
    self._reset()

  def _reset(self):
    """
    self.nodes = preorder traversal of nodes
    self.history = element i was discovered or finished at time i
    self.pos = position of vertices in animate
    """
    self.nodes, self.node_to_edge_labels, self.history = {}, {}, []
    self.id, self.time, self.depth = 0, 0, 0
    self.cache = {}
    self.func_name = ''

  def _animate(self, history, nodes, node_to_edge_labels, func_name):
    DG = get_graph(history, nodes, node_to_edge_labels)

    # # create recursion tree animation
    # fig = animate(history, nodes, func_name)
    # fig.show()

    # # save figure
    # if self.save:
    #   if self.path == '':
    #     input = ','.join(list(map(str, nodes[0]['input'])))
    #     self.path = './{}_{}.html'.format(func_name, input)
    #   fig.write_html(self.path)

  def __call__(self, 
               func: callable # function to be visualized or cached via decorator
               ):
    """A custom `__call__` function records the id, function input, function output, depth, discovery time, 
    and finish time in a node each time the function is called. After all function calls are made, `__call__`
    will animate the recursion tree. This is the main workhorse of the `RecursionVisualizer` class.
    
    At a high-level, the `__call__` function looks something like:
    
    ```
    def __call__(self, func):
      def memoized_func(*args, **kwargs):
        # record discovery time, function input, and depth
        node.discovery = time
        node.input = args
        node.depth = depth
        
        # if node not in cache, compute and cache result
        if node not in self.cache:
          self.cache[args] = func(*args, **kwargs)
          
        # record finish time and function output
        node.output = self.cache[args]
        node.finish = time
        
        if depth == 0:
          animate()
        
      return memoized_func
    ```
    """

    def memoized_func(*args, **kwargs):
      if self.depth == 0:
        self._reset()

      # record node's depth, discovery time, and input arguments
      id_ = len(self.nodes)
      node = Node(id_=id_, input=args, depth=self.depth, discovery=self.time)
      self.history.append(node.id_)
      self.nodes[node.id_] = node
      self.time += 1

      # update depth and call the function `func`
      self.depth += 1
      # if args not in self.cache:
      self.cache[args] = func(*args, **kwargs)
      self.depth -= 1

      # record node's output, finish time, history, and edge_label
      self.nodes[id_].output = self.cache[args]
      self.nodes[id_].finish = self.time
      
      self.node_to_edge_labels[id_] = kwargs['edge_label'] if kwargs and 'edge_label' in kwargs else ''
      self.history.append(node.id_)
      self.time += 1

      if self.verbose:
        print(node)

      # animate after done traversing through the entire tree
      if self.animate and self.depth == 0:
        self._animate(self.history, self.nodes, self.node_to_edge_labels, func.__name__)

      return self.cache[args]
    return memoized_func