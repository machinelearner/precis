from unittest import TestCase
from gensim import corpora
from gensim.models import LdaModel, LsiModel

import logging
from precis.utils import CosineSimilarity

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)


class LDATest(TestCase):
    def test_shouldCreateLDAModel(self):
        documents = [['human', 'interface', 'computer'],
                     ['survey', 'user', 'computer', 'system', 'response', 'time'],
                     ['eps', 'user', 'interface', 'system'],
                     ['system', 'human', 'system', 'eps'],
                     ['user', 'response', 'time'],
                     ['trees'],
                     ['graph', 'trees'],
                     ['graph', 'minors', 'trees'],
                     ['graph', 'minors', 'survey']]

        dicitonary = corpora.Dictionary(documents)
        corpus = []
        for doc in documents:
            corpus.append(dicitonary.doc2bow(doc))

        lda_model = LdaModel(corpus=corpus,id2word=dicitonary,num_topics=20, passes=100)



        for doc in corpus:
            print lda_model[doc]

        print "############### Corpus #################"
        print corpus
        print dicitonary.token2id
        print "############### Querying #################"


        score_vector_matrix = []
        for doc in corpus:
            aux_vec = []
            for token, val in lda_model[doc]:
                aux_vec.append(val)
            score_vector_matrix.append(aux_vec)

        for i in range(0,8):
            for j in range(i+1, 9):
                cos_sim = CosineSimilarity().calculate(score_vector_matrix[i], score_vector_matrix[j])
                print "(" + str(i) + ", " + str(j) + ") : " + str(cos_sim)



        print "############### New Document Query #################"
        new_doc = ['computer', 'minors', 'survey', 'graph', 'trees']
        lda_vec = lda_model[dicitonary.doc2bow(new_doc)]
        new_vector = [val for id, val in lda_vec]
        for j in range(0, 9):
            cos_sim = CosineSimilarity().calculate(new_vector, score_vector_matrix[j])
            print "(new doc" + str(j) + ") : " + str(cos_sim)