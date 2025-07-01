import random
from numpy.random import permutation


def random_permutations(n, count):
    return [list(map(int, permutation(n))) for i in range(count)]


class StripPackingGenAlg:
    def __init__(self, data, parameters):
        self.width = data["width"]
        self.rects = ["rectangles"]
        self.pop_size = parameters["population_size"]
        self.generations = parameters["generations"]
        self.best_solution = list()
        self.population = list()
        self.pop_suitability = list()
        self.cross_prob = parameters["crossover_prob"]
        self.mut_prob = parameters["mutation_prob"]
        self.sample_size = parameters["sample_size"]
        self.avg_suitability = list()
        self.min_suitability = list()
        self.cur_generation = -1

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
        return max_len, placed

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
        self.best_solution.append(self.population[min_ind])

    def crossover(self, gene1, gene2):
        if random.random() > self.cross_prob:
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
        if random.random() > self.mut_prob:
            return gene
        n = len(gene)
        p1, p2 = random.randint(0, n - 1), random.randint(0, n - 1)
        while p1 == p2:
            p2 = random.randint(0, n - 1)
        gene_new = gene.copy()
        gene_new[p1], gene_new[p2] = gene_new[p2], gene_new[p1]
        return gene_new

     #Стохастическая выборка по ранжированным вероятностям
    def sample(self):
        parents = list()
        #Сортировка популяции по убыванию ф-ии приспособленности - элементы левее имеют меньший ранг
        sorted_pop = sorted(zip(self.population, self.pop_suitability), key=lambda x: x[1], reverse=True)
        cumulative = [(n+1)*n//2 for n in range(self.pop_size+1)] # кумулятивные суммы рангов
        s = cumulative[self.pop_size]
        step = s / self.pop_size # шаг выборки
        position = random.randint(0,s)/self.pop_size # начальная позиция от 0 до s/N
        ind = 0
        while position <= s:
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
            if pair_ind >= self.sample_size-1:
                pair_ind = 0
                random.shuffle(parents)
            descendants.extend(self.crossover(parents[pair_ind], parents[pair_ind+1]))
            pair_ind += 1
        for i in range(self.pop_size):
            descendants[i] = self.mutation(descendants[i])
        self.population = descendants[:self.pop_size]
        self.update_suitability()

    def get_best_solution(self):
        return self.best_solution[-1], self.place_rectangles(self.best_solution[-1])

    def next_step(self):
        if self.cur_generation == -1:
            self.population = random_permutations(len(self.rects), self.pop_size)
        elif self.cur_generation == self.generations-1:
            return False
        else:
            self.new_population()
        self.cur_generation += 1
        return True

    def execute(self):
        for _ in range(self.cur_generation, self.generations-1):
            self.next_step()

    def get_data(self):
        return {"n": len(self.rects), "width": self.width, "rectangles": self.rects}

    def status(self):
        if self.cur_generation == self.generations-1:
            return "finished"
        else:
            return "in progress"