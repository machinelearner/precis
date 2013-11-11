from precis.core import Synonyms, TFIDFMeasure
from precis.core import ConnectedNodes
from precis.text import SentenceGraph


class Summarizer:
    DISSIMILARITY_THRESHOLD = 0.8

    def __init__(self, ):
        self.dissimilar_sentences = SentenceGraph()

    def semantic_summary(self, tokenised_sentence_dict):
        print "Building Dissimilar Sentences Graph"
        self.build_dissimilarity_graph_using_wordnet(tokenised_sentence_dict)
        print "Dissimilar Sentences Graph build complete"
        cliques = self.dissimilar_sentences.find_cliques()
        print cliques
        return list(cliques)[0]
        #TODO Return Sentences belonging to maximal clique

    def simple_summary(self, tokenised_sentence_dict):
        print "Building Dissimilar Sentences Graph"
        self.build_simple_dissimilarity_graph(tokenised_sentence_dict)
        print "Dissimilar Sentences Graph build complete"
        cliques = self.dissimilar_sentences.find_cliques()
        print cliques
        return list(cliques)[0]
        #TODO Return Sentences belonging to maximal clique

    def community_summary(self, tokenised_sentence_dict):
        print "Building Dissimilar Sentences Graph"
        self.build_simple_dissimilarity_graph(tokenised_sentence_dict)
        print "Dissimilar Sentences Graph build complete"
        communities = self.dissimilar_sentences.multilevel_communities()
        for community in communities:
            print community

    def build_dissimilarity_graph_using_wordnet(self, tokenised_sentence_dict):
        sentence_keys = tokenised_sentence_dict.keys()
        synonyms = Synonyms(tokenised_sentence_dict.values())
        self.dissimilar_sentences.add_nodes(sentence_keys)
        connections = ConnectedNodes()
        edges = list()
        for every_key, tokens in tokenised_sentence_dict.iteritems():
            for other_key, other_tokens in tokenised_sentence_dict.iteritems():
                if connections.not_connected(every_key, other_key):
                    score = synonyms.dissimilarity_score(tokens, other_tokens)
                    if score > self.DISSIMILARITY_THRESHOLD:
                        edge = (every_key, other_key, {"weight": score})
                        edges.append(edge)
                        connections.add((every_key, other_key))
        self.dissimilar_sentences.add_edges(edges)


    def build_simple_dissimilarity_graph(self, tokenised_sentence_dict):
        sentence_keys = tokenised_sentence_dict.keys()
        tfidf_measure = TFIDFMeasure(tokenised_sentence_dict)
        self.dissimilar_sentences.add_nodes(sentence_keys)
        connections = ConnectedNodes()
        edges = list()
        for every_key, tokens in tokenised_sentence_dict.iteritems():
            for other_key, other_tokens in tokenised_sentence_dict.iteritems():
                if connections.not_connected(every_key, other_key):
                    score = tfidf_measure.dissimilarity_score(tokens, other_tokens)
                    if score > self.DISSIMILARITY_THRESHOLD:
                        edge = (every_key, other_key, {"weight": score})
                        edges.append(edge)
                        connections.add((every_key, other_key))
        self.dissimilar_sentences.add_edges(edges)
