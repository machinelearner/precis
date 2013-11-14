from collections import defaultdict
from gensim import corpora
from gensim.models import LdaModel, ldamodel
from precis.utils import CosineSimilarity


class LDATransformation:

    def __init__(self, input_space_vectors):
        self.input_space_vectors = input_space_vectors
        self.transform()

    def transform(self):
        self.space = corpora.Dictionary(self.input_space_vectors)
        #TODO Handle Saner Reduction
        #self.reduced_space = 3 if len(self.space)/100 < 3 else len(self.space)/10
        self.reduced_space = 15

        input_BOWs = [self.space.doc2bow(vector) for vector in self.input_space_vectors]
        self.lda_model = LdaModel(corpus=input_BOWs, id2word=self.space, num_topics=self.reduced_space, passes=100)

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

