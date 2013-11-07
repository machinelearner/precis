from multiprocessing import Process, Pool, Queue
from precis.text import TextProcessor
from precis.text import Sets


class Synonyms:
    def __init__(self, list_of_tokens):
        set_of_tokens = Sets.union_all(list_of_tokens)
        self.synonyms = TextProcessor.synonyms_for(set_of_tokens)

    def dissimilarity_score(self, tokens, other_tokens):
        word_combinations = 1
        dissimilarity_score = 0
        for a_word in tokens:
            a_synset = self.synonyms[a_word]
            for other_word in other_tokens:
                other_synset = self.synonyms[other_word]
                if a_word != other_word:
                    word_combinations += 1
                    dissimilarity_score += (1 - self.calculate_max_wup_similarity(a_synset, other_synset))
        return dissimilarity_score / word_combinations

    def calculate_max_wup_similarity(self, sysnet_1, sysnet_2):
        max_similarity = 0
        for syns1 in sysnet_1:
            for syns2 in sysnet_2:
                similarity_score = syns1.wup_similarity(syns2)
                if similarity_score > max_similarity:
                    max_similarity = similarity_score
        return max_similarity

    def dissimilarity_score_parallel(self, tokens, other_tokens):
        # WordNet is not thread-safe; Waste of time this!!
        synonyms = self.synonyms
        wup_score_calc_pool = Pool(4)
        synset_pairs = []
        for a_word in tokens:
            synset_pairs += [(synonyms[a_word], synonyms[other_word]) for
                             other_word in other_tokens if a_word is not other_word]
        wup_scores = wup_score_calc_pool.imap_unordered(calculate_max_wup_similarity, synset_pairs)
        #dissimilarity_score = reduce(lambda x, y: x+y, wup_scores)
        dissimilarity_score = 0
        for val in wup_scores:
            dissimilarity_score += val

        word_combinations = len(wup_scores)
        return dissimilarity_score / word_combinations


def calculate_max_wup_similarity((synset_1, synset_2)):
    max_similarity = 0
    for syns1 in synset_1:
        for syns2 in synset_2:
            similarity_score = syns1.wup_similarity(syns2)
            if similarity_score > max_similarity:
                max_similarity = similarity_score
    return max_similarity
