from unittest import TestCase
from precis.core import Synonyms


class TestSynonyms(TestCase):
    def test_shouldGetDissimilarityFaster(self):
        list_of_tokens = [["movie", "expected", "more", "disappointed"], ["horrible", "great", "fantastic", "car"]]
        synonyms = Synonyms(list_of_tokens)
        score = synonyms.dissimilarity_score(["fantastic", "car"], ["horrible", "movie"])
        self.assertIsNotNone(score)
