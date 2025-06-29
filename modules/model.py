import random
from numpy.random import permutation


def random_permutations(n, count):
    return [list(map(int, permutation(n))) for i in range(count)]


def place_rectangles(order, rects, width):
    placed = []

    for i in order:
        w, h = rects[i]
        x, y = 0, 0

    # Слева направо, снизу вверх
        while True:
            overlaps = False
            for px, py, pw, ph in placed:
                if not (x + w <= px or x >= px + pw or y + h <= py or y >= py + ph):
                    overlaps = True
                    break
            if not overlaps and x + w <= width:
                placed.append((x, y, w, h))
                break
            x += 1
            if x + w > width:
                x = 0
                y += 1
            if y > 1000000:
                return None, None
    max_len = max(y + h for x, y, w, h in placed)
    return max_len, placed


class StripPackingGenAlg:
    def __init__(self, width, rectangles, population_size=100, generations=100):
        self.strip_width = width
        self.rectangles = rectangles
        self.population_size = population_size
        self.generations = generations
        self.displayed_solution = None

    #Функция приспособленности - число, обратное длине размещения прямоугольников
    def suitability(self, order):
        length = place_rectangles(order)[0]
        return 1 / length

    def crossover(self, gene1, gene2):
        n = len(gene1)
        p1, p2 = random.randint(0, n - 1), random.randint(0, n - 1)
        p1, p2 = min(p1, p2), max(p1, p2)
        gene_new1, gene_new2 = [-1] * n, [-1] * n
        for i in range(p1, p2 + 1):
            gene_new1[i], gene_new2[i] = gene2[i], gene1[i]
        gene1_cut = set(gene1[p1:p2 + 1])
        gene2_cut = set(gene2[p1:p2 + 1])
        i, j = 0, 0
        while i < n:
            if gene_new1[i] == -1:
                if gene1[j] not in gene2_cut:
                    gene_new1[i] = gene1[j]
                j += 1
            else:
                i += 1
        i, j = 0, 0
        while i < n:
            if gene_new2[i] == -1:
                if gene2[j] not in gene1_cut:
                    gene_new2[i] = gene2[j]
                j += 1
            else:
                i += 1
        print(p1, p2)
        return gene_new1, gene_new2

    def mutation(self, gene):
        n = len(gene)
        p1, p2 = random.randint(0, n - 1), random.randint(0, n - 1)
        while p1 == p2:
            p2 = random.randint(0, n - 1)
        gene_new = gene.copy()
        gene_new[p1], gene_new[p2] = gene_new[p2], gene_new[p1]
        return gene_new
