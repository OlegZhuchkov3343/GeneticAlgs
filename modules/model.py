import random
from numpy.random import permutation


def random_permutations(n, count):
    return [permutation(n) for i in range(count)]


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
