from collections import defaultdict
from unittest import TestCase
from precis.core.lsi_transformation import LSITransformation
from precis.text import TextProcessor
from precis.utils import FileReader


class LSITest(TestCase):

    def test_shouldCheckForConsistencyOfLSIModel(self):
        import os
        filepath = os.path.join(os.path.dirname(__file__), "test_data/reuters_rupee_decline/doc1")
        text = FileReader.read(filepath)
        processor = TextProcessor()
        sentences = processor.nltk_sentences(text)
        tokenised_sentence_map = dict(
            [(index, processor.stopped_tokenize(sentence)) for index, sentence in enumerate(sentences)])


        for i in range(5):
            print "\n\n************* ITERATION ", i, " *************"
            lsi_transformation = LSITransformation(tokenised_sentence_map)
            lsi_transformation.print_transformation()