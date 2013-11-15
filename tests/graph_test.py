from unittest import TestCase
from igraph import VertexClustering, Graph
from precis.text import SentenceGraph


class GraphTest(TestCase):
    def test_shouldReturnCommunityLevelWithMaximumCommunities(self):
        graph_1 = Graph()
        graph_1.add_vertices(["1","2","3","4"])
        graph_1.add_edges([("1","2"),("2","4"),("1","4"),("2","3")])
        graph_2 = Graph()
        graph_2.add_vertices(["1","3","4"])
        graph_2.add_edges([("3","4"),("1","4"),("1","3")])
        vertex_clustering_1 = VertexClustering(graph_1)
        vertex_clustering_2 = VertexClustering(graph_2)

        community_levels = [vertex_clustering_1, vertex_clustering_2]
        expected_communities = vertex_clustering_1
        actual_communities = SentenceGraph().find_best_community_level(community_levels)

        self.assertEquals(actual_communities, expected_communities)
