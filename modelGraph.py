import tkinter as tk
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from tableau_procedure import KripkeModel


class GraphVisualization(tk.Frame):
    """
    Visualize the Kripke Model as a graph.
    
    Parameters
    ----------
    parent: tk.Tk
        Tkinter GUI object.
    model: KripkeModel
        Kripke Model object.

    """
    def __init__(self, parent, model:KripkeModel, *args, **kwargs):
        
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create the graph
        G = nx.DiGraph()
        for world in model.worlds:
            G.add_node(world.name, values=world.values)

        for world, connections in model.relations.items():
            for connection in connections:
                G.add_edge(world, connection)


        lbls={n:v["values"] for n,v in G.nodes(data=True)}
        no_incoming_edges = [node for node in G.nodes() if not list(G.predecessors(node))]
        node_colors = ['#6ABD56' if node in no_incoming_edges else 'green' for node in G.nodes()]
        
        # Draw the graph
        plt.figure()
        pos = nx.circular_layout(G)
        nx.draw(G, pos,labels=lbls, arrows=True, style='', margins=0.05,
                arrowstyle=patches.ArrowStyle('Fancy', head_length=5, head_width=2.5, tail_width=0.4),
                font_weight='bold', font_color='black',font_size=20, 
                node_color=node_colors, node_size=3000,
                edge_color='black', width=6)
        
        # Add the graph to the Tkinter GUI
        canvas = FigureCanvasTkAgg(plt.gcf(), self)
        canvas.draw()
        self.graph = canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

