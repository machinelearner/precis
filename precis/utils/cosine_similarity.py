from math import sqrt


class CosineSimilarity:

    def mod(self, vector):
        sum_of_squares = 0
        for coordinate in vector:
            sum_of_squares += pow(coordinate, 2)
        return sqrt(sum_of_squares)

    def calculate(self, vector1, vector2):
        mod_vector1 = self.mod(vector1)
        mod_vector2 = self.mod(vector2)
        dot_product = 0
        for i in range(0, len(vector1)):
            dot_product += vector1[i] * vector2[i]

        return dot_product / (mod_vector1 * mod_vector2)
