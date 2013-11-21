from collections import defaultdict
from unittest import TestCase
from gensim import corpora
from gensim.models import LdaModel

from precis.core.lda_transformation import LDATransformation
from precis.utils import CosineSimilarity


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

    def test_shouldCheckForConsistencyOfLDAModel(self):
        tokenised_documents_dict = defaultdict();

        #tokenised_documents_dict["sent1"] = ["liked", "Kevin", "Costner", "great", "job", "movie"]
        #tokenised_documents_dict["sent2"] = ["felt", "Ashton", "great", "job", "liked"]
        #tokenised_documents_dict["sent3"] = ["pleasantly", "surprised", "Kevin", "Costner", "Ashton", "Kutcher", "find", "movie", "showing", "sneak", "preview", "local", "theater"]

        tokenised_documents_dict["sent1"] = ["human", "machine", "interface", "lab", "abc", "computer", "applications"]
        tokenised_documents_dict["sent2"] = ["survey", "user", "opinion", "computer", "system", "response", "time"]
        tokenised_documents_dict["sent3"] = ["EPS", "user", "interface", "management", "system"]
        tokenised_documents_dict["sent4"] = ["system", "human", "system", "engineering", "testing", "EPS"]
        tokenised_documents_dict["sent5"] = ["Relation", "user", "perceived", "response", "time", "error", "measurement"]
        tokenised_documents_dict["sent6"] = ["generation", "random", "binary", "unordered", "trees"]
        tokenised_documents_dict["sent7"] = ["intersection", "Graph", "paths", "trees"]
        tokenised_documents_dict["sent8"] = ["Graph", "minors", "IV", "Widths", "trees", "quasi", "ordering"]
        tokenised_documents_dict["sent9"] = ["Graph", "minors", "survey"]

        for i in range(5):
            print "\n\n************* ITERATION " + str(i) + " *************"
            lda_transformation = LDATransformation(tokenised_documents_dict);
            lda_model = lda_transformation.transform()
            topics = lda_model.show_topics(topn=20)
            for topic in topics:
                print topic