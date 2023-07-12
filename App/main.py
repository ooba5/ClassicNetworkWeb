import numpy as np
from flask import Flask, render_template, session, request,redirect, url_for
import networkx as nx
from pyvis.network import Network
import matplotlib.colors
from settings import Config
app = Flask("pythonProject")
app.secret_key = Config.secret

@app.route("/")
def home():
    if session.get("book") is None:
        session["book"] = "Dracula"
    G = nx.read_gml(f"Data/{session['book']}_graph.gml")
    net = Network("800px", "100%", bgcolor="black", font_color="#999999")

    cnorm = matplotlib.colors.Normalize(1, len(G) + 1)
    cmap = matplotlib.cm.ScalarMappable(norm=cnorm, cmap="RdBu")

    for node in G.nodes(data=True):
        net.add_node(node[0].title(), size=node[1]["weight"] / len(G.nodes),
                     color=matplotlib.colors.to_hex(cmap.to_rgba(node[1]["sentiment"]))
                     )

    all_sents = [e[2]["sentiment"] for e in G.edges(data=True)]
    all_weights = [e[2]["weight"] for e in G.edges(data=True)]
    cut_off = np.percentile(all_weights, 50)
    cnorm_edge = matplotlib.colors.Normalize(min(all_sents), max(all_sents))
    cmap_edge = matplotlib.cm.ScalarMappable(norm=cnorm_edge, cmap="RdBu")

    for edge in G.edges(data=True):

        if edge[2]["weight"] > cut_off:
            net.add_edge(edge[0].title(), edge[1].title(), value=edge[2]["weight"] * 100,
                         color=matplotlib.colors.to_hex(cmap_edge.to_rgba(edge[2]["sentiment"])))
    return render_template("home.html", viz=net.generate_html())

@app.route("/book", methods=["POST"])
def book():
    content = request.json
    session["book"] = content["name"]
    return "OK"



if __name__ == "__main__":

    app.run()