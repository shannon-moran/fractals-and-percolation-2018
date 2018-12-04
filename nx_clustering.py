def connected_components(G):
    """Generate connected components.
    Parameters
    ----------
    G : NetworkX graph
       An undirected graph
    Returns
    -------
    comp : generator of sets
       A generator of sets of nodes, one for each component of G.
    Raises
    ------
    NetworkXNotImplemented:
        If G is directed.
    Examples
    --------
    Generate a sorted list of connected components, largest first.
    >>> G = nx.path_graph(4)
    >>> nx.add_path(G, [10, 11, 12])
    >>> [len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)]
    [4, 3]
    If you only want the largest connected component, it's more
    efficient to use max instead of sort.
    >>> largest_cc = max(nx.connected_components(G), key=len)
    See Also
    --------
    strongly_connected_components
    weakly_connected_components
    Notes
    -----
    For undirected graphs only.
    """
    seen = set()
    for v in G:
        if v not in seen:
            c = set(_plain_bfs(G, v))
            yield c
            seen.update(c)

def node_connected_component(G, n):
    """Return the set of nodes in the component of graph containing node n.
    Parameters
    ----------
    G : NetworkX Graph
       An undirected graph.
    n : node label
       A node in G
    Returns
    -------
    comp : set
       A set of nodes in the component of G containing node n.
    Raises
    ------
    NetworkXNotImplemented:
        If G is directed.
    See Also
    --------
    connected_components
    Notes
    -----
    For undirected graphs only.
    """
    return set(_plain_bfs(G, n))

# breadth-first search
def _plain_bfs(G, source):
    """A fast BFS node generator"""
    G_adj = G.adj
    seen = set()
    nextlevel = {source}
    while nextlevel:
        thislevel = nextlevel
        nextlevel = set()
        for v in thislevel:
            if v not in seen:
                yield v
                seen.add(v)
                nextlevel.update(G_adj[v])
