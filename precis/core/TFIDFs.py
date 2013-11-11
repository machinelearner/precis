from collections import defaultdict
from precis.utils import CosineSimilarity


class TFIDFMeasure:
    def __init__(self, map_of_sentences):
        self.sentences = map_of_sentences
        self.tfidf = self.compute()
        self.space = self.tfidf.keys()

    def dissimilarity_score(self, tokens, other_tokens):
        vector1 = self.vectorize(tokens)
        vector2 = self.vectorize(other_tokens)
        cosine_similarity_score = CosineSimilarity().calculate(vector1, vector2)
        return 1-cosine_similarity_score

    def similarity_score(self, tokens, other_tokens):
        vector1 = self.vectorize(tokens)
        vector2 = self.vectorize(other_tokens)
        cosine_similarity_score = CosineSimilarity().calculate(vector1, vector2)
        return cosine_similarity_score

    def vectorize(self,tokens):
        vector = [0] * len(self.space)
        for i, dimension in enumerate(self.space):
            if dimension in tokens:
                vector[i] = self.tfidf[dimension]
        return vector

    def compute(self):
        word_freq = defaultdict(int)
        inverted_index = defaultdict(set)
        for sentence_key, token_list in self.sentences.iteritems():
            for token in token_list:
                word_freq[token] += 1
                doc_id = sentence_key.split("_")[0]
                inverted_index[token].add(doc_id)

        tfidf = defaultdict(float)
        max_tfidf = 0
        for token, frequency in word_freq.iteritems():
            token_tfidf = frequency / float(len(inverted_index[token]))
            tfidf[token] = token_tfidf
            if token_tfidf > max_tfidf:
                max_tfidf = token_tfidf
        return self.normalise(tfidf, max_tfidf)

    def normalise(self, tfidf_map, max_tfidf):
        normalised_tfidf = defaultdict(float)
        for token, tfidf in tfidf_map.iteritems():
            normalised_tfidf[token] = tfidf/float(max_tfidf)
        return normalised_tfidf