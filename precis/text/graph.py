import networkx

class SentenceGraph():
    _graph = networkx.Graph()
    def add_nodes(self,sentence_numbers):
        self._graph.add_nodes_from(sentence_numbers)

    def add_edge(self,edge_3_tuple):
        """

        @type edge_3_tuple: (from_node,to_node,dict({"weight":value}))
        """
        self._graph.add_edge(edge_3_tuple)

    def find_cliques(self):
        cliques = networkx.find_cliques_recursive(self._graph)
        return cliques

    def add_edges(self, edges):
        self._graph.add_edges_from(edges)
