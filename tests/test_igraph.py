from unittest import TestCase
from igraph import Graph


class TestIGraph(TestCase):
    def test_should(self):
        graph = Graph()
        graph.add_vertices(["1", "2"])
        graph.add_edge("1", "2",weight=9)
        self.assertFalse(graph.is_directed())