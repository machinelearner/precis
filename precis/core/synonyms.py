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

    def calculate_max_wup_similarity(self, word1_synsets, word2_synsets):
        max_similarity = 0
        for syns1 in word1_synsets:
            for syns2 in word2_synsets:
                similarity_score = syns1.wup_similarity(syns2)
                if similarity_score > max_similarity:
                    max_similarity = similarity_score
        return max_similarity
