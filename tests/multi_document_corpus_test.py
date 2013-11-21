from unittest import TestCase
import os.path as ospath
from precis.core import Document, MultiDocumentCorpus, MultiDocument


class TestMultiDocumentCorpus(TestCase):
    def setUp(self):
        self.test_documents_path = ospath.join(ospath.dirname(__file__), "test_data/multi_document_test")


    def test_shouldCreateMultiDocumentGivenADirectoryPath(self):
        document_text1 = """This is content of the file1\nWith line separated. blabla !!!"""
        document_text2 = """This is content of the file.\nWith line separated. blabla"""
        document1 = Document(id="1.txt", text=document_text1)
        document2 = Document(id="2.txt", text=document_text2)
        expected_multi_document = MultiDocument(documents=[document1, document2])

        actual_multi_document = MultiDocumentCorpus(self.test_documents_path).multi_document()

        self.assertEquals(actual_multi_document, expected_multi_document)

    def generateSummaries(self):
        test_documents_path = ospath.join(ospath.dirname(__file__), "test_data/summarize_multi_document_test")
        documents = MultiDocumentCorpus(test_documents_path).multi_document()
        documents.summarize_and_print()

    def test_generateConnectedSummaries(self):
        test_documents_path = ospath.join(ospath.dirname(__file__), "test_data/summarize_multi_document_test")
        documents = MultiDocumentCorpus(test_documents_path).multi_document()
        summary = documents.summarize_using_communities()
        for sent in summary:
            print sent

    def generateConnectedSummariesOfReutersNewsArticles(self):
        test_documents_path = ospath.join(ospath.dirname(__file__), "test_data/reuters_rupee_decline")
        documents = MultiDocumentCorpus(test_documents_path).multi_document()
        summary = documents.summarize_using_communities()
        for sent in summary:
            print sent