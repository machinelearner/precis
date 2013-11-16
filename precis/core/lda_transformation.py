from collections import defaultdict
import operator
from gensim.models import LdaModel
from precis.utils import CosineSimilarity


class LDASpace():
    def __init__(self, tokenised_documents):
        self.token_frequency_map = self.token_frequency(tokenised_documents)
        self.id_2_word, self.token_2_id = self.compute_id_word_mappings()

    def normalise(self, frequency_map):
        normalised_frequency_map = defaultdict(float)
        max_frequency = max(frequency_map.iteritems(), key=operator.itemgetter(1))[1]
        map(lambda (token, frequency): normalised_frequency_map.update({token: frequency / float(max_frequency)}),
            list(frequency_map.iteritems()))
        return normalised_frequency_map

    def id2Word(self):
        return self.id_2_word

    def doc2bow(self, vector):
        return [(self.token_2_id[token], self.token_frequency_map[token]) for token in vector]

    def token_frequency(self, tokenised_documents):
        word_freq = defaultdict(int)
        for token_list in tokenised_documents:
            map(lambda token: word_freq.update({token: word_freq[token] + 1}), token_list)
        #return self.normalise(word_freq)
        return word_freq

    def compute_id_word_mappings(self):
        sorted_tokens = sorted(self.token_frequency_map.iteritems(), key=operator.itemgetter(0))
        token_2_id_map = dict([(token, i) for i, (token, freq) in enumerate(sorted_tokens)])
        id_2_token_map = dict([(i, token) for i, (token, freq) in enumerate(sorted_tokens)])
        return id_2_token_map, token_2_id_map


class LDATransformation:

    def __init__(self, input_space_vectors_map):
        self.input_space_vectors = input_space_vectors_map.values()
        self.transform()

    def transform(self):
        self.space = LDASpace(self.input_space_vectors)
        #TODO Handle Saner Reduction
        #self.reduced_space = 3 if len(self.space)/100 < 3 else len(self.space)/10
        self.reduced_space = 15

        input_BOWs = [self.space.doc2bow(vector) for vector in self.input_space_vectors]
        self.lda_model = LdaModel(corpus=input_BOWs, id2word=self.space.id2Word(), num_topics=self.reduced_space, passes=100)

    def dissimilarity_score(self, tokens, other_tokens):
        bows = self.space.doc2bow(tokens)
        other_bows = self.space.doc2bow(other_tokens)

        vector = self.infer_and_vectorize(bows)
        other_vector = self.infer_and_vectorize(other_bows)
        similarity = CosineSimilarity().calculate(vector, other_vector)
        return 1 - similarity

    def infer_and_vectorize(self, bows):
        transformed_bow = defaultdict(float)
        transformed_bow.update(dict(self.lda_model[bows]))
        return [transformed_bow[dimension] for dimension in range(0, self.reduced_space)]

