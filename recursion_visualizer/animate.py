# AUTOGENERATED! DO NOT EDIT! File to edit: ../02_animate.ipynb.

# %% auto 0
__all__ = ['get_node_and_edge_coordinates', 'get_node_text', 'get_edge_text', 'get_link_annotation', 'get_title', 'get_slider',
           'update_slider', 'get_play_pause_buttons', 'get_axis_settings', 'animate']

# %% ../02_animate.ipynb 2
from .node import Node 
from .graph import get_graph

# %% ../02_animate.ipynb 3
import networkx as nx
import plotly.graph_objects as go

from typing import List, Dict
from plotly.subplots import make_subplots

# %% ../02_animate.ipynb 5
def get_node_and_edge_coordinates(
  DG, # `networkx` graph of recursive function calls
  ) -> List[List[int]]: # list of x and y coordinates for placing nodes and edges on 2D plot
  """Given a map of edges to labels, create a `networkx` graph and use its
  layout function to return a list of x and y coordinates for placing nodes and edges on
  a 2D plot."""

  # get the (x, y) coordinates of each node in the graph
  coordinates = nx.drawing.nx_agraph.graphviz_layout(DG, prog="dot", root=0)

  # record the (x, y) coordinates of each node
  node_x, node_y = [], []
  for x, y in coordinates.values():
    node_x.append(x)
    node_y.append(y)

  # record the (x, y) coordinates of each edge
  edge_x, edge_y = [], []
  for edge in DG.edges():
        x0, y0 = coordinates[edge[0]]
        x1, y1 = coordinates[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

  return node_x, node_y, edge_x, edge_y

# %% ../02_animate.ipynb 7
def get_node_text(
   nodes: Dict[int, Node], # map of node ids to nodes
   func_name: str, # name of the recursive function
   display_args
   ) -> List[List[str]]: # text(s) to be displayed on each node
   """Return the text(s) to be displayed on each node. Specifically, return
  
   1. `max_node_length`: the length of the longest node annotation text; used to
      determine the size of the node (in pixels)
   2. `node_annotations`: the text that appears in each node; this is set to be the
      input to the recursive function
   3. `hovertext`: the text that appears when the user hovers over a node in
      the graph; this is set to the input+output to the recursive function and the
      discovery+finish times of the recursive function.
   """
  
   hovertext, node_annotations = [], []
   max_node_length = 0

   for node in nodes.values():
      
      # get arguments to the recursive function
      # if `display_args` is a list, only display the ith argument if i is in `display_args`
      input_ = list(map(str, node.input))
      if isinstance(display_args, list):
         input_ = [input_[arg_idx] for arg_idx in display_args]
      function_input = ','.join(input_)
      
      text = '{}({})={}'.format(func_name, function_input, node.output)
      text += '<br>discover: {}<br>finish: {}'.format(node.discovered, node.finish)

      node_annotations.append(function_input)
      max_node_length = max(max_node_length, len(function_input))
      hovertext.append(text)
   return max_node_length, node_annotations, hovertext

# %% ../02_animate.ipynb 8
def get_edge_text(
      node_x: List[int], # x coordinates of nodes
      node_y: List[int], # y coordinates of nodes
      edge_to_label: Dict[tuple, str], # map of edges to labels (edge is a tuple of two node ids)
      ) -> List[str]: # text(s) to be displayed on each edge
      """Return the text(s) to be displayed on each edge. This is optional and
      by default will display an empty string along each edge. Specifically, return
      
      1. `edge_text`: the text that appears along each edge; this is set to be
         `edge_label`, a keyword found in the decorated recursive function.
      """

      # initial values
      buffer = 5
      edge_annotations = []

      for i, ((node1, node2), label) in enumerate(edge_to_label.items()):
            x1, y1 = node_x[node1], node_y[node1]
            x2, y2 = node_x[node2], node_y[node2]
            edge_annotations.append(
                  dict(text=label,
                        x=(x1+x2)/2 + buffer, y=(y1+y2)/2 + buffer,
                        xref='x1', yref='y1',
                        font=dict(color='rgb(0,0,0)', size=10),
                        showarrow=False)
                  )
      return edge_annotations    

# %% ../02_animate.ipynb 9
def get_link_annotation(
    ) -> List[dict]: # text that links to this library's GitHub repo
    """Return the (formatted) text that links to this library's GitHub repo."""
    
    return [dict(
        text="Made with <a href='https://github.com/ez2rok/recursion-visualizer'>Recursion Visualizer</a>",
        showarrow=False,
        x=0.005, y=-0.002,
        xref="paper", yref="paper",
        )
    ]

# %% ../02_animate.ipynb 10
def get_title(
    nodes: Dict[int, Node], # map of node ids to nodes
    func_name: str, # name of the recursive function
    ) -> str: # title of the graph
    """Return the (formatted) title of the graph"""
    
    function_input = ','.join(list(map(str, nodes[0].input)))
    title_text = 'Recursive Tree: {}({})'.format(func_name, function_input)
    return {
        'text': title_text,
        'y':0.95,
        'x':0.02,
        'xanchor': 'left',
        'yanchor': 'top'
        }

# %% ../02_animate.ipynb 12
def get_slider() -> dict: # slider to control the animation
  """Return the slider that allows the user to control the animation"""
    
  return {
      "active": 0,
      "yanchor": "top",
      "xanchor": "left",
      "currentvalue": {
          "font": {"size": 20},
          "prefix": "Time:",
          "visible": True,
          "xanchor": "right"
      },
      "transition": {"duration": 300, "easing": "cubic-in-out"},
      "pad": {"b": 5, "t": 5},
      "len": 0.9,
      "x": 0.1,
      "y": 0,
      "steps": []
  }

# %% ../02_animate.ipynb 13
def update_slider(
  slider: dict, # slider that allows the user to control the animation 
  time: int, # current time
  ) -> dict: # updated slider
  """Update the slider with the current time"""
    
  slider_step = {
      "args": [[time],
               {"frame": {"duration": 300, "redraw": False},
                "mode": "immediate",
                "transition": {"duration": 300}}
               ],
               "label": time,
                "method": "animate"
                }
  slider["steps"].append(slider_step)

# %% ../02_animate.ipynb 14
def get_play_pause_buttons() -> List[dict]: # play/pause buttons
    """Return the play/pause buttons
    
    **References**:
    
    1. Heavily inspired by [Plotly animation
       tutorial](https://plotly.com/python/animations/#using-a-slider-and-buttons)
    """
    return [
    {"buttons": 
     [{"args": [None, {"frame": {"duration": 500, "redraw": False},
                       "fromcurrent": True, 
                       "transition": {"duration": 300, "easing": "quadratic-in-out"}
                       }
                ],
       "label": "Play",
       "method": "animate"
       },
      {"args": [[None], {"frame": {"duration": 0, "redraw": False},
                         "mode": "immediate",
                         "transition": {"duration": 0}
                         }
                ],
       "label": "Pause",
       "method": "animate"
       }
      ],
     "direction": "up",
     "pad": {"r": 20, "t": 15},
     "showactive": True,
     "type": "buttons",
     "x": 0.1,
     "xanchor": "right",
     "y": 0,
     "yanchor": "top"
     }
     ]

# %% ../02_animate.ipynb 15
def get_axis_settings() -> dict: # axis settings
  """Return the axis settings"""
  
  return dict(showline=False,
              zeroline=False,
              showgrid=False,
              showticklabels=False
              )

# %% ../02_animate.ipynb 17
def animate(history,nodes,
            func_name, 
            DG, 
            edge_to_label,
            display_args
            ):
  
  # get node and edge coordinates
  node_x, node_y, edge_x, edge_y = get_node_and_edge_coordinates(DG)
  
  # get text to be displayed on the nodes, edges, and figure
  max_node_length, node_annotations, hovertext = get_node_text(nodes, func_name, display_args)
  edge_annotations = get_edge_text(node_x, node_y, edge_to_label)
  link_annotation = get_link_annotation()
  title = get_title(nodes, func_name)
  
  # get graphics
  slider = get_slider()
  axis_settings = get_axis_settings()
  buttons = get_play_pause_buttons()

  # keep track of the visit status of each node at each time step:
  #   0 -> unvisited
  #   1 -> visiting
  #   2 -> visited
  # This is used to color the node circles and the node text.
  visit = [0] * len(nodes)
  visit_to_text_color =  {0: 'rgb(0,0,0)', 1: 'rgb(255, 255, 255)', 2: 'rgb(255, 255, 255)'}
  node_text_color = [visit_to_text_color[visit[id_]] for id_ in nodes.keys()]

  # get frames
  frames = []
  fig = make_subplots(specs=[[{"secondary_y": True}]])
  for time, node_id in enumerate([None] + history):
    
    # update visit status, node text color, and circle color
    # Note: circle color is determined by `visit`` so by updating `visit`, we've updated circle color
    if node_id != None:
      visit[node_id] += 1
      node_text_color[node_id] = visit_to_text_color[visit[node_id]]

    # plot nodes
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hovertext=hovertext,
        hoverinfo='text',
        text=node_annotations,
        #textfont={'color': node_annotation_colors[time]},
        textfont={'color': node_text_color},
        marker={'line': dict(color='rgb(50,50,50)', width=1),
                'color': visit,
                'cmid': 1,
                'colorscale': [(0.00, '#F7FBFF'), (0.33, '#F7FBFF'),
                               (0.33, '#6AAED6'), (0.66, '#6AAED6'),
                               (0.66, '#0A306B'), (1.00, '#0A306B')
                               ], # colors taken from px.colors.sequential.Blues
                'size': 10 + 7*max_node_length},
        showlegend=False,
        ids=list(nodes.keys())
        )
    
    # plot edges
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines',
        showlegend=False,
        textposition="bottom right"
        )
    
    # updates frames and slider
    frame = go.Frame(data=[node_trace, edge_trace], name=str(time))
    frames.append(frame)
    update_slider(slider, time)

  # create layout
  layout = go.Layout(
      title=title,
      xaxis=axis_settings,
      yaxis=axis_settings,
      annotations=link_annotation+edge_annotations,
      margin=dict(b=0,l=5,r=5,t=5),
      updatemenus=buttons,
      sliders=[slider]
      )

  fig = go.Figure(data=frames[0]['data'], layout=layout, frames=frames[1:])
  return fig
