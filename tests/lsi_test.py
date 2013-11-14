from unittest import TestCase
from gensim import utils, corpora
from gensim.models import LsiModel, LdaModel

import logging
from precis.utils.cosine_similarity import CosineSimilarity

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class LSITest(TestCase):
    def test_shouldCreateSimpleLsiModel(self):
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

        lsi_model = LsiModel(corpus=corpus,id2word=dicitonary,num_topics=6)
        lsi_model.print_topics()
        print "############### Querying #################"
        #for doc in corpus:
        #    print lsi_model[doc]
        #print lsi_model[corpus[8]]

        score_vector_matrix = []
        for doc in corpus:
            aux_vec = []
            for token, val in lsi_model[doc]:
                aux_vec.append(val)
            score_vector_matrix.append(aux_vec)

        for i in range(0,8):
            for j in range(i+1, 9):
                cos_sim = CosineSimilarity().calculate(score_vector_matrix[i], score_vector_matrix[j])
                print "(" + str(i) + ", " + str(j) + ") : " + str(cos_sim)

        #print CosineSimilarity().calculate(score_vector_matrix[7], score_vector_matrix[8])