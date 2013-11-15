from igraph import Graph
import networkx

class SentenceGraph():
    WEIGHT = "weight"
    _graph = Graph()

    def add_nodes(self, sentence_numbers):
        self._graph.add_vertices(sentence_numbers)

    def add_edge(self, edge_3_tuple):
        """

        @type edge_3_tuple: (from_node,to_node,dict({"weight":value}))
        """
        self._graph.add_edge(edge_3_tuple[0],edge_3_tuple[1], weight=edge_3_tuple[2][self.WEIGHT])

    def add_edges(self, edges):
        map(lambda edge: self.add_edge(edge), edges)

    def multilevel_communities(self):
        return self._graph.community_multilevel(weights=self.WEIGHT, return_levels=True)

    def find_best_community_level(self, community_levels):
        best_community_level_index = 0
        for community_level_index, communities in enumerate(community_levels):
            if len(communities) > len(community_levels[best_community_level_index]):
                best_community_level_index = community_level_index
        return community_levels[best_community_level_index]
