import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

f = open("paths.processed.csv")

for line in f.readlines():
    l = line.strip()
    if l:
        n_from, n_to = l.split(',')
        if n_from != '???' and n_to != '???' and not n_to.startswith("192.168.1"):
            G.add_edge(n_from, n_to)

leaves = [x for x in G.nodes() if G.out_degree(x) == 0]

print([x for x in G.nodes() if G.in_degree(x) == 0])

routers = {}

for leaf in leaves:
    node_routers = G.predecessors(leaf)
    for node_router in node_routers:
        if node_router in routers.keys():
            routers[node_router] = routers[node_router] + 1
        else:
            routers[node_router] = 1
        G.remove_node(leaf)

render_leaves = []
render_leaves_labels = {}

for router in routers.keys():
    G.add_edge(router, router + "-" + str(routers[router]))
    render_leaves.append(router + "-" + str(routers[router]))
    render_leaves_labels[router + "-" +
                         str(routers[router])] = str(routers[router])

G = G.to_undirected()

cliques = list(sorted([s for s in nx.find_cliques(G)
               if len(s) > 3], key=len, reverse=True))

merged_cliques = []

for clique in cliques:
    overlap = False
    for merged_clique in merged_cliques:
        if bool(set(clique) & set(merged_clique)):
            overlap = True
    if not overlap:
        merged_cliques.append(clique)

merged_node = []
merged_labels = {}

for idx, merged_clique in enumerate(merged_cliques):
    G.add_node('merged-node-' + str(idx))
    merged_node.append('merged-node-' + str(idx))
    merged_labels['merged-node-' + str(idx)] = "clique-" + str(idx)
    for node in merged_clique:
        neis = list(nx.neighbors(G, node))
        for nei in neis:
            G.add_edge('merged-node-' + str(idx), nei)
        G.remove_node(node)

G.remove_edges_from(nx.selfloop_edges(G))
G.remove_nodes_from(list(nx.isolates(G)))

pos = nx.spring_layout(G)

plt.plot()

local_nodes = ["192.168.1.1"]
local_labels = {
    "192.168.1.1": "local"
}

nx.draw_networkx_nodes(
    G, pos, nodelist=local_nodes, node_color="tab:purple")
nx.draw_networkx_nodes(
    G, pos, nodelist=merged_node, node_color="tab:orange")
nx.draw_networkx_nodes(
    G, pos, nodelist=render_leaves, node_color="tab:red")
nx.draw_networkx_nodes(
    G, pos, nodelist=[n for n in G.nodes if n not in render_leaves + merged_node + local_nodes], node_color="tab:blue")
nx.draw_networkx_labels(G, pos, labels=render_leaves_labels)
nx.draw_networkx_labels(G, pos, labels=local_labels)
nx.draw_networkx_labels(G, pos, labels=merged_labels)
nx.draw_networkx_edges(G, pos, arrows=False, alpha=0.5)

plt.show()
