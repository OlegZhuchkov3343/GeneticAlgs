import random
from numpy.random import permutation


def random_permutations(n, count):
    return [list(map(int, permutation(n))) for i in range(count)]


class StripPackingGenAlg:
    def __init__(self, data, parameters):
        self.width = data["width"]
        self.rects = data["rectangles"]
        self.pop_size = int(parameters["population_size"])
        self.generations = int(parameters["generations"])
        self.best_solution = list()
        self.population = list()
        self.pop_suitability = list()
        self.cross_prob = parameters["crossover_prob"]
        self.mut_prob = parameters["mutation_prob"]
        self.sample_size = int(parameters["sample_size"])
        self.avg_suitability = list()
        self.min_suitability = list()
        self.cur_generation = -1
        self.diff = parameters["diff"]
        self.gen_history = list()

    def place_rectangles(self, order):
        placed = []

        for i in order:
            w, h = self.rects[i]
            x, y = 0, 0

            # Слева направо, снизу вверх
            while True:
                overlaps = False
                for px, py, pw, ph in placed:
                    if not (x + w <= px or x >= px + pw or y + h <= py or y >= py + ph):
                        overlaps = True
                        break
                if not overlaps and x + w <= self.width:
                    placed.append((x, y, w, h))
                    break
                x += 1
                if x + w > self.width:
                    x = 0
                    y += 1
                if y > 1000000:
                    return None, None
        max_len = max(y + h for x, y, w, h in placed)
        ordered = zip(order, placed)
        ordered = [rect[1] for rect in sorted(ordered)]
        return max_len, ordered

    #Функция приспособленности - длина размещения прямоугольников, задача - минимизировать значение функции
    def suitability(self, order):
        length = self.place_rectangles(order)[0]
        return length

    def update_suitability(self):
        self.pop_suitability = [self.suitability(order) for order in self.population]
        minimum = min(self.pop_suitability)
        min_ind = self.pop_suitability.index(minimum)
        avg = sum(self.pop_suitability)/self.pop_size
        self.min_suitability.append(minimum)
        self.avg_suitability.append(avg)
        self.best_solution.append((self.population[min_ind], self.pop_suitability[min_ind]))

    def crossover(self, gene1, gene2):
        rand = random.random()
        if rand > self.cross_prob:
            return gene1, gene2
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
        return gene_new1, gene_new2

    def mutation(self, gene):
        rand = random.random()
        if rand > self.mut_prob:
            return gene
        n = len(gene)
        p1, p2 = random.randint(0, n - 1), random.randint(0, n - 1)
        while p1 == p2:
            p2 = random.randint(0, n - 1)
        gene_new = gene.copy()
        gene_new[p1], gene_new[p2] = gene[p2], gene[p1]
        return gene_new

     #Стохастическая выборка по ранжированным вероятностям
    def sample(self):
        parents = list()
        #Сортировка популяции по убыванию ф-ии приспособленности - элементы левее имеют меньший ранг
        sorted_pop = sorted(zip(self.population, self.pop_suitability), key=lambda x: x[1], reverse=True)
        cumulative = [(n+1)*n//2 for n in range(1, self.pop_size+2)] # кумулятивные суммы рангов
        s = cumulative[self.pop_size]
        step = s / self.sample_size # шаг выборки
        position = random.randint(0,s)/self.sample_size # начальная позиция от 0 до s/N
        ind = 0
        if position < cumulative[0]:
            parents.append(sorted_pop[ind][0])
            position += step
        while position <= s and ind < self.pop_size:
            if cumulative[ind] <= position < cumulative[ind+1]:
                parents.append(sorted_pop[ind][0])
                position += step
            else:
                ind += 1
        return parents

    def new_population(self):
        parents = self.sample()
        descendants = list()
        random.shuffle(parents)
        pair_ind = 0
        while len(descendants) < self.pop_size:
            if pair_ind >= self.sample_size-2:
                pair_ind = 0
                random.shuffle(parents)
            descendants.extend(self.crossover(parents[pair_ind], parents[pair_ind+1]))
            pair_ind += 2
        for i in range(self.pop_size):
            descendants[i] = self.mutation(descendants[i])
        self.population = descendants[:self.pop_size]
        self.update_suitability()

    def get_best_solution(self):
        return min(self.best_solution, key=lambda x: x[1])

    def next_step(self):
        if self.cur_generation == -1:
            self.population = random_permutations(len(self.rects), self.pop_size)
            self.update_suitability()
        else:
            self.new_population()
        self.cur_generation += 1
        self.gen_history.append(self.population)

    def step_back(self):
        self.population = self.gen_history[-2]
        self.cur_generation -= 1
        self.gen_history.pop(-1)
        self.avg_suitability.pop(-1)
        self.min_suitability.pop(-1)
        self.best_solution.pop(-1)

    def get_data(self):
        return {"n": len(self.rects), "width": self.width, "rectangles": self.rects}

    def status(self):
        if self.cur_generation == -1:
            return "init"
        elif self.cur_generation == self.generations-1 and self.avg_suitability[-1] - self.min_suitability[-1] < self.diff:
            return "generation+diff limit"
        elif self.cur_generation == self.generations-1:
            return "generation limit"
        elif self.avg_suitability[-1] - self.min_suitability[-1] < self.diff:
            return "diff limit"
        else:
            return "in progress"

    def get_info(self):
        info = {
            "rect_count": len(self.rects),
            "width": self.width,
            "pop_size": self.pop_size,
            "sample_size": self.sample_size,
            "generations": self.generations,
            "best_solution": self.place_rectangles(self.best_solution[-1][0]),
            "cross_prob": self.cross_prob,
            "mut_prob": self.mut_prob,
            "avg_suitability": self.avg_suitability,
            "min_suitability": self.min_suitability,
            "cur_generation": self.cur_generation+1,
            "diff": self.diff
        }
        return info
