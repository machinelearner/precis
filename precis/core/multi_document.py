from collections import defaultdict
import os
from precis.core import Document, Summarizer
from precis.utils import FileReader


class MultiDocument:
    def __init__(self, documents=None, summarizer=Summarizer()):
        if not documents: documents = list()
        if not isinstance(documents[0], Document): raise RuntimeError(
            "Illegal MultiDocument, A Multi Document is a collection of Documents")
        self.documents = documents
        self.summarizer = summarizer

    def raw_sentences(self):
        sentences = defaultdict(str)
        for document in self.documents:
            sentences.update(document.sentence_dict())
        return sentences

    def tokenised_sentences(self):
        sentences = defaultdict(list)
        for document in self.documents:
            sentences.update(document.tokenised_sentences_dict())
        return sentences

    def summarize(self):
        tokenised_sentences = self.tokenised_sentences()
        raw_sentences = self.raw_sentences()
        sentences_in_summary = self.summarizer.simple_summary(tokenised_sentences)
        summary = []
        for sentence in sentences_in_summary:
            summary.append(raw_sentences[sentence])
        return summary

    def summarize_using_communities(self):
        tokenised_sentences = self.tokenised_sentences()
        raw_sentences = self.raw_sentences()
        summary_sentence_ids = self.summarizer.community_summary(tokenised_sentences)
        summary = [raw_sentences[sentence] for sentence in summary_sentence_ids]
        return summary

    def summarize_and_print(self):
        summary_sentences = self.summarize()
        print "=======================Summary======================="
        for sentence in summary_sentences:
            print sentence

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and set(self.documents) == set(other.documents))

    def __ne__(self, other):
        return not self.__eq__(other)


class MultiDocumentCorpus:
    def __init__(self, directory_path):
        self.path = directory_path

    def multi_document(self):
        text_files = []
        documents = []
        for root, dirs, files in os.walk(self.path):
            text_files += map(lambda file_name: os.path.join(root, file_name), files)
        for doc_no, filepath in enumerate(text_files):
            text = FileReader.read(filepath)
            documents.append(Document(id=doc_no, text=text))

        return MultiDocument(documents=documents)

