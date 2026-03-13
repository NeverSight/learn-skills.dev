---
name: networkx
description: Python package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks. Supports various graph types (Directed, Undirected, Multigraphs) and features a vast library of standard graph algorithms. Use for network analysis, graph theory, social network analysis, biological networks, infrastructure networks, path finding, centrality measures, community detection, graph algorithms, shortest paths, PageRank, connectivity analysis, and routing optimization.
version: 3.2
license: BSD-3-Clause
---

# NetworkX - Network Analysis and Graph Theory

NetworkX is the go-to library for analyzing complex networks. It treats graphs as flexible containers for nodes (any hashable object) and edges, which can carry arbitrary metadata.

## When to Use

- Analyzing social, biological, or infrastructure networks.
- Calculating path metrics (shortest paths, diameters, flow).
- Measuring node importance (Centrality, PageRank).
- Detecting communities and clusters within a network.
- Generating random graph models (Erdős-Rényi, Barabási-Albert).
- Finding connectivity components and cliques.
- Designing and optimizing routing or dependency trees.

## Reference Documentation

**Official docs**: https://networkx.org/  
**Algorithm reference**: https://networkx.org/documentation/stable/reference/algorithms/index.html  
**Search patterns**: `nx.Graph`, `nx.shortest_path`, `nx.degree_centrality`, `nx.connected_components`

## Core Principles

### Graph Types

| Class | Description |
|-------|-------------|
| `Graph` | Undirected graph; ignores self-loops if added twice. |
| `DiGraph` | Directed graph; edges have a specific direction (A → B ≠ B → A). |
| `MultiGraph` | Undirected; allows multiple edges between the same two nodes. |
| `MultiDiGraph` | Directed; multiple directed edges between nodes. |

### Nodes and Edges

- **Nodes**: Can be any hashable Python object (strings, numbers, tuples, even objects).
- **Edges**: Represent a relationship between two nodes. Can store attributes like weight, capacity, or label.

## Quick Reference

### Installation

```bash
pip install networkx matplotlib scipy
```

### Standard Imports

```python
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
```

### Basic Pattern - Creation and Analysis

```python
import networkx as nx

# 1. Create a graph
G = nx.Graph()

# 2. Add edges (nodes are created automatically)
G.add_edge("A", "B", weight=4.5)
G.add_edges_from([("B", "C"), ("C", "A"), ("C", "D")])

# 3. Analyze
print(f"Nodes: {G.number_of_nodes()}")
print(f"Shortest path A to D: {nx.shortest_path(G, 'A', 'D')}")

# 4. Draw
nx.draw(G, with_labels=True)
```

## Critical Rules

### ✅ DO

- **Use weighted edges** - For any real-world distance or cost analysis.
- **Check Connectivity** - Always verify `nx.is_connected(G)` before running algorithms that assume a single component.
- **Set the right Class** - Use `DiGraph` if the direction of interaction matters (e.g., website links, metabolic pathways).
- **Use Sparse Matrices** - For heavy computation, export to SciPy sparse matrices using `nx.to_scipy_sparse_array`.
- **Attribute access** - Use `G.nodes[n]['attr']` or `G.edges[u, v]['attr']` to store/retrieve metadata.
- **Node Immutability** - Ensure node objects are hashable and their state doesn't change if used as keys.

### ❌ DON'T

- **Use for high-performance viz** - `nx.draw` is for small debug plots. Use Gephi or Cytoscape for large-scale visualization.
- **Manual Path Loops** - Avoid writing your own BFS/DFS; NetworkX's built-in algorithms are highly optimized.
- **Store Large Objects in nodes** - Keep nodes simple (ID); store complex data in a separate dictionary if possible to save memory.
- **Ignore Graph Generators** - Don't create complex synthetic graphs manually; use `nx.random_graphs`.

## Anti-Patterns (NEVER)

```python
import networkx as nx

# ❌ BAD: Manual neighbor iteration for degree calculation
count = 0
for n in G.nodes():
    for neighbor in G.neighbors(n):
        count += 1

# ✅ GOOD: Use built-in degree property
degrees = dict(G.degree())

# ❌ BAD: Re-calculating shortest paths in a loop
for target in targets:
    path = nx.dijkstra_path(G, source, target) # Re-scans graph every time

# ✅ GOOD: Calculate single-source shortest paths once
paths = nx.single_source_dijkstra_path(G, source)
# 'paths' now contains the shortest path to every reachable node

# ❌ BAD: Using lists for edges in large graphs
# (Creating a graph from a massive edge list one by one is slow)

# ✅ GOOD: Bulk loading
G.add_edges_from(edge_list)
```

## Algorithms Deep Dive

### Shortest Paths and Flow

```python
# Shortest path with weights (Dijkstra)
path = nx.shortest_path(G, source="A", target="D", weight="weight")
length = nx.shortest_path_length(G, source="A", target="D", weight="weight")

# All-pairs shortest paths (returns a generator)
all_paths = dict(nx.all_pairs_dijkstra_path(G))

# Max Flow / Min Cut
from networkx.algorithms.flow import preflow_push
flow_value, flow_dict = nx.maximum_flow(G, "source_node", "sink_node", capacity="cap")
```

### Centrality and Importance

```python
# Degree Centrality (fraction of nodes it's connected to)
deg_cent = nx.degree_centrality(G)

# Betweenness Centrality (importance as a bridge/bottleneck)
bet_cent = nx.betweenness_centrality(G)

# PageRank (influence in directed networks)
pagerank = nx.pagerank(G, alpha=0.85)

# Eigenvector Centrality
eig_cent = nx.eigenvector_centrality(G)
```

### Community Detection and Clustering

```python
# Clustering coefficient (measure of "tightness")
avg_clustering = nx.average_clustering(G)

# Community detection (Girvan-Newman)
from networkx.algorithms import community
comp = community.girvan_newman(G)
top_level_communities = next(comp)

# Louvain Community Detection (standard for large networks)
# requires: pip install python-louvain
communities = community.louvain_communities(G)
```

### Connectivity and Components

```python
# Undirected components
components = list(nx.connected_components(G))
largest_cc = max(components, key=len)

# Directed connectivity
is_strong = nx.is_strongly_connected(DG) # Path in both directions
is_weak = nx.is_weakly_connected(DG)     # Path if direction is ignored

# Cliques (fully connected subgraphs)
cliques = list(nx.find_cliques(G))
```

## Graph I/O and Interoperability

### Formats and Converters

```python
# Reading/Writing files
nx.write_gexf(G, "network.gexf")   # For Gephi
nx.write_graphml(G, "data.graphml") # For general graph tools
G = nx.read_edgelist("edges.txt")   # From simple text file

# Integration with Pandas
df = nx.to_pandas_edgelist(G)
G_new = nx.from_pandas_edgelist(df, source='source', target='target', edge_attr='weight')

# Integration with NumPy/SciPy
adj_matrix = nx.to_numpy_array(G)
sparse_adj = nx.to_scipy_sparse_array(G)
```

## Practical Workflows

### 1. Analyzing Protein-Protein Interaction (PPI) Networks

```python
def analyze_ppi(edge_list_file):
    G = nx.read_edgelist(edge_list_file)
    
    # 1. Basic stats
    print(f"Network density: {nx.density(G):.4f}")
    
    # 2. Find hubs (high degree)
    degree_dict = dict(G.degree())
    hubs = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # 3. Find essential clusters
    communities = nx.community.louvain_communities(G)
    
    # 4. Check for articulation points (bottlenecks)
    bottlenecks = list(nx.articulation_points(G))
    
    return hubs, communities, bottlenecks
```

### 2. Transport Routing with Constraints

```python
def find_route(G, start, end, max_load):
    """Find shortest path that respects a capacity constraint."""
    # Filter edges by capacity
    view = nx.subgraph_view(G, filter_edge=lambda u, v: G[u][v]['capacity'] >= max_load)
    
    if not nx.has_path(view, start, end):
        return None
    
    return nx.shortest_path(view, start, end, weight='distance')
```

### 3. Visualizing Hierarchical Structures

```python
def plot_tree(G, root):
    """Custom layout for tree-like structures."""
    pos = nx.spring_layout(G) # Basic layout
    # Or use graphviz for better tree layouts
    # pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=500, font_size=10, arrowsize=20)
    plt.show()
```

## Performance Optimization

### Using Graph Views

Instead of creating copies of the graph when filtering nodes/edges, use a "view" which is O(1) in time and memory.

```python
# Create a view of the graph with only heavy edges
heavy_edges = nx.subgraph_view(G, filter_edge=lambda u, v: G[u][v]['weight'] > 10)
```

### Efficient Node Access

When iterating over nodes and their attributes, use `data=True`.

```python
# Faster than calling G.nodes[n] inside the loop
for n, attrs in G.nodes(data=True):
    if attrs.get('type') == 'target':
        do_something(n)
```

## Common Pitfalls and Solutions

### Dictionary modification during iteration

```python
# ❌ Problem: Changing the graph while looping over nodes
for n in G.nodes():
    if G.degree(n) == 0:
        G.remove_node(n) # Error!

# ✅ Solution: Convert nodes to a list first
for n in list(G.nodes()):
    if G.degree(n) == 0:
        G.remove_node(n)
```

### Self-loops and Multi-edges in simple Graphs

```python
# ❌ Problem: Adding a second edge between A and B in nx.Graph() 
G.add_edge("A", "B", weight=10)
G.add_edge("A", "B", weight=20) # Overwrites the first weight!

# ✅ Solution: Use MultiGraph if multiple relations exist
MG = nx.MultiGraph()
MG.add_edge("A", "B", weight=10)
MG.add_edge("A", "B", weight=20) # Both are preserved
```

### Directionality in flow algorithms

```python
# ❌ Problem: Running PageRank on an Undirected graph
# It works, but it's just a scaled degree centrality.

# ✅ Solution: Ensure you use DiGraph for influence metrics
DG = nx.DiGraph(G) # Converts undirected to directed with symmetric edges
```

NetworkX provides the perfect balance between ease of use and algorithmic depth. Whether you are solving a small logic puzzle or analyzing a complex biological system, it provides the tools to understand the underlying structure of your data.
