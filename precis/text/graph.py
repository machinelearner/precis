from igraph import Graph
import networkx

class SentenceGraph():
    WEIGHT = "weight"
    _graph = Graph()
    def add_nodes(self, sentence_numbers):
        self._graph.add_vertices(sentence_numbers)

    def add_edge(self,edge_3_tuple):
        """

        @type edge_3_tuple: (from_node,to_node,dict({"weight":value}))
        """
        self._graph.add_edge(edge_3_tuple[0],edge_3_tuple[1], weight=edge_3_tuple[2][self.WEIGHT])

    @DeprecationWarning
    def find_cliques(self):
        cliques = networkx.find_cliques(self._graph)
        return cliques

    @DeprecationWarning
    def most_connected_component(self):
        graph = networkx.DiGraph(self._graph)
        connected_components = networkx.strongly_connected_components(graph)
        return connected_components[0]

    def add_edges(self, edges):
        map(lambda edge: self.add_edge(edge), edges)

    def multilevel_communities(self):
        #return self._graph.community_multilevel(weights=self.WEIGHT, return_levels=True)
        return self._graph.community_spinglass(weights=self.WEIGHT)
