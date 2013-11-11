from unittest import TestCase
from precis.utils import CosineSimilarity


class TestCosineSimilarity(TestCase):
    def test_should_calculate_mod_of_a_vector(self):
        vector = [3, 4, 5, 5, 5]
        expected_mod = 10.0
        actual_mod = CosineSimilarity().mod(vector)
        self.assertEquals(actual_mod, expected_mod)

    def test_should_calculate_cosine_similarity_of_two_vectors(self):
        vector1 = [3, 4, 5, 5, 5]
        vector2 = [3, 2, 1, 1, 1]
        expected_score = 0.8
        actual_score = CosineSimilarity().calculate(vector1, vector2)
        self.assertEquals(actual_score, expected_score)
