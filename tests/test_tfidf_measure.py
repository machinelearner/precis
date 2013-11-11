from unittest import TestCase
from precis.core import TFIDFMeasure


class TestTFIDFMeasure(TestCase):
    def test_should_compute_tfidf_for_sentence_dictionary(self):
        tokenised_sentence_map = {"doc1_sent1": ["man", "river", "drown"], "doc1_sent2": ["man", "sea", "dive"],
                                  "doc1_sent3": ["man", "river", "man"],
                                  "doc2_sent1": ["dog", "river", "dive"], "doc2_sent2": ["man", "dog", "dog"],
                                  "doc3_sent1": ["man", "sea", "drown"]
        }
        expected_tf = {
            "man": 6,
            "river": 3,
            "drown": 2,
            "sea": 2,
            "dive": 2,
            "dog": 3
        }
        expected_df = {
            "man": 3,
            "river": 2,
            "drown": 2,
            "sea": 2,
            "dive": 2,
            "dog": 1
        }
        expected_tfidf = {
            "man": 2,
            "river": 1.5,
            "drown": 1,
            "sea": 1,
            "dive": 1,
            "dog": 3
        }
        expected_normalised_tfidf = {
            "man": 2/3.0,
            "river": 0.5,
            "drown": 1/3.0,
            "sea": 1/3.0,
            "dive": 1/3.0,
            "dog": 1
        }

        tfidf_measure = TFIDFMeasure(tokenised_sentence_map)

        actual_tfidf = tfidf_measure.compute()

        self.assertEquals(actual_tfidf,expected_normalised_tfidf)