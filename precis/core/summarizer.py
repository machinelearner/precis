from precis.core import Synonyms
from precis.core import ConnectedNodes
from precis.core.lsi_transformation import LSITransformation
from precis.text import SentenceGraph, TextProcessor


class Summarizer:
    DISSIMILARITY_THRESHOLD = 0.8

    def __init__(self, transformation=LSITransformation):
        self.dissimilar_sentences = SentenceGraph()
        self.transformation = transformation

    def semantic_summary(self, tokenised_sentence_dict):
        print "Building Dissimilar Sentences Graph"
        self.build_dissimilarity_graph_using_wordnet(tokenised_sentence_dict)
        print "Dissimilar Sentences Graph build complete"
        cliques = self.dissimilar_sentences.multilevel_communities()
        print cliques
        return list(cliques)[0]
        #TODO Return Sentences

    def community_summary(self, tokenised_sentence_dict):
        self.build_dissimilarity_graph(tokenised_sentence_dict)
        community_levels = self.dissimilar_sentences.multilevel_communities()
        best_community = self.best_community(community_levels, tokenised_sentence_dict)
        return best_community.vs["name"]

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

    def build_dissimilarity_graph(self, tokenised_sentence_dict):
        print "Building Dissimilar Sentences Graph"
        sentence_keys = tokenised_sentence_dict.keys()
        transformed_sentences = self.transformation(tokenised_sentence_dict)
        self.dissimilar_sentences.add_nodes(sentence_keys)
        connections = ConnectedNodes()
        edges = list()
        for every_key, tokens in tokenised_sentence_dict.iteritems():
            for other_key, other_tokens in tokenised_sentence_dict.iteritems():
                if connections.not_connected(every_key, other_key):
                    score = transformed_sentences.dissimilarity_score(tokens, other_tokens)
                    if score > self.DISSIMILARITY_THRESHOLD:
                        edge = (every_key, other_key, {"weight": score})
                        edges.append(edge)
                        connections.add((every_key, other_key))
        self.dissimilar_sentences.add_edges(edges)
        print "Dissimilar Sentences Graph build complete"

    def best_community(self, community_levels, tokenised_sentences_dict):
        best_communities = self.dissimilar_sentences.find_best_community_level(community_levels)
        communities_subgraphs = best_communities.subgraphs()
        best_community_id = 0
        best_community_index = 0.0
        text_processor = TextProcessor()
        for id, community in enumerate(communities_subgraphs):
            vertices = community.vs["name"]
            sigma_info_index = 0.0
            for vertex in vertices:
                sentence = tokenised_sentences_dict[vertex]
                info_index = text_processor.information_index(sentence)
                sigma_info_index += info_index
            sigma_info_index /= float(len(vertices))
            if best_community_index < sigma_info_index:
                best_community_index = sigma_info_index
                best_community_id = id

        return communities_subgraphs[best_community_id]



