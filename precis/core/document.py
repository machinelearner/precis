from collections import defaultdict
from precis.text import TextProcessor
from precis.utils import FileReader
import os


class Document:
    def __init__(self, id=0,text="",text_processor=TextProcessor()):
        self.id = id
        self.text = text
        self.text_processor = text_processor

    def sentence_dict(self):
        sentences = defaultdict(str)
        sentence_list = self.text_processor.sent_tokenize(self.text)
        for id,sentence in enumerate(sentence_list):
            sentences[self.sent_hashKey(id)] = sentence
        return sentences

    def tokenised_sentences_dict(self):
        sentences = defaultdict(list)
        sentence_list = self.text_processor.sent_tokenize(self.text)
        for id,sentence in enumerate(sentence_list):
            sentences[self.sent_hashKey(id)] = self.text_processor.stopped_tokenize(sentence)
        return sentences

    def sent_hashKey(self,sent_number):
        return "doc" + str(self.id) + "-" + "sent" + str(sent_number)


    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)
