from collections import defaultdict
import operator
from gensim.models import LsiModel
import numpy
from precis.utils import CosineSimilarity


class LSISpace():
    def __init__(self, tokenised_documents):
        self.token_frequency_map = self.token_frequency(tokenised_documents)
        self.id_2_word, self.token_2_id = self.compute_id_word_mappings()

    def prune(self, frequency_map):
        pruned_frequency_map = defaultdict(int)
        mean_frequency = numpy.asarray(frequency_map.values()).mean()
        standard_deviation = numpy.asarray(frequency_map.values()).std()
        for key, value in frequency_map.iteritems():
            if self.is_frequency_significant(value, mean_frequency, standard_deviation):
                pruned_frequency_map[key] = value
        return pruned_frequency_map

    def id2Word(self):
        return self.id_2_word

    def doc2bow(self, vector):
        return [(self.token_2_id[token], self.token_frequency_map[token]) for token in vector]

    def token_frequency(self, tokenised_documents):
        word_freq = defaultdict(int)
        for token_list in tokenised_documents:
            map(lambda token: word_freq.update({token: word_freq[token] + 1}), token_list)
        #return self.prune(word_freq)
        return word_freq

    def compute_id_word_mappings(self):
        sorted_tokens = sorted(self.token_frequency_map.iteritems(), key=operator.itemgetter(0))
        token_2_id_map = defaultdict(int, [(token, i) for i, (token, freq) in enumerate(sorted_tokens)])
        id_2_token_map = defaultdict(int, [(i, token) for i, (token, freq) in enumerate(sorted_tokens)])
        return id_2_token_map, token_2_id_map

    def is_frequency_significant(self, value, mean, dev):
        if (value < mean - dev) or (value > mean + dev):
            return False
        return True

    def length(self):
        return len(self.token_2_id.keys())


class LSITransformation:
    def __init__(self, input_space_vectors_map):
        self.input_space_vectors = input_space_vectors_map.values()
        self.transform()

    def transform(self):
        self.space = LSISpace(self.input_space_vectors)
        #TODO Handle Saner Reduction
        self.reduced_space = 15

        input_BOWs = [self.space.doc2bow(vector) for vector in self.input_space_vectors]
        self.lsi_model = LsiModel(corpus=input_BOWs, num_topics=self.reduced_space, id2word=self.space.id2Word())
        return self.lsi_model

    def dissimilarity_score(self, tokens, other_tokens):
        bows = self.space.doc2bow(tokens)
        other_bows = self.space.doc2bow(other_tokens)

        vector = self.infer_and_vectorize(bows)
        other_vector = self.infer_and_vectorize(other_bows)
        similarity = CosineSimilarity().calculate(vector, other_vector)
        return 1 - similarity

    def infer_and_vectorize(self, bows):
        transformed_bow = defaultdict(float)
        transformed_bow.update(dict(self.lsi_model[bows]))
        return [transformed_bow[dimension] for dimension in range(0, self.reduced_space)]

    def print_transformation(self):
        topics = self.lsi_model.show_topics(num_words=self.space.length(), formatted=False)
        for topic in topics:
                print [(round(value, 4), token) for value, token in topic]