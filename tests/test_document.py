from unittest import TestCase
from mockito import mock, when, verify
from precis.core import Document


class TestDocument(TestCase):
    def test_shouldGetSentenceDictionary(self):
        sample_text = "This is a sample peice of text. This should get split into two sentences"
        sample_sentences = ["This is a sample peice of text","This should get split into two sentences"]
        expected_sentence_dict = {
            "doc123-sent0" : sample_sentences[0],
            "doc123-sent1" : sample_sentences[1]
        }
        mockProcessor = mock()

        when(mockProcessor).nltk_sentences(sample_text).thenReturn(sample_sentences)
        when(mockProcessor).remove_non_ascii(sample_text).thenReturn(sample_text)
        test_document = Document(id=123,text=sample_text,text_processor=mockProcessor)

        actual_sentence_dict = test_document.sentence_dict()
        self.assertEquals(actual_sentence_dict,expected_sentence_dict)
        verify(mockProcessor).nltk_sentences(sample_text)