import numpy as np
import random


# based on the java code proposed by Lee Jacobson
# http://www.theprojectspot.com/tutorial-post/applying-a-genetic-algorithm-to-the-travelling-salesman-problem/5


class Individual:

    def __init__(self, dist_matrix, order=None):
        self.mtx = dist_matrix
        self.order = order
        if order is None:
            points = [point for point in range(1, len(dist_matrix))]
            random.shuffle(points)
            self.order = points

    def __repr__(self):
        res = [0]
        res.extend(self.order)
        res.append(0)
        return str(res)

    @property
    def size(self):
        return len(self.mtx) - 1

    @property
    def fitness(self):
        return 1.0 / self.distance

    @property
    def distance(self):
        total_distance = self.mtx[0][self.order[0]] + self.mtx[self.order[-1]][0]
        if self.size > 1:
            for i in range(1, self.size):
                total_distance += self.mtx[self.order[i - 1]][self.order[i]]
        return total_distance

    def set_place(self, pos, place):
        self.order[pos] = place


class Population:

    def __init__(self, dist_matrix, size):
        self.individuals = [Individual(dist_matrix=dist_matrix)
                            for _ in range(size)]

    @property
    def size(self):
        return len(self.individuals)

    def fittest(self):
        best = self.individuals[0]
        for individual in self.individuals[1:]:
            if best.fitness < individual.fitness:
                best = individual
        return best


class GA:

    def __init__(self, mtx=None,
                 population_size=100, generations_number=50,
                 mutation_rate=0.01, tournament_size=5, elitism=True):
        self.mtx = mtx
        self.population_size = population_size
        self.generations_number = generations_number
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.elitism = elitism

    def evolve(self, verbose=True):
        population = Population(self.mtx, self.population_size)
        if verbose:
            winner = population.fittest()
            print(0, winner, winner.distance)
        for gn in range(self.generations_number):
            new_population = Population(self.mtx, self.population_size)
            # keep the best individual if elitism is enabled
            elitism_offset = 0
            if self.elitism:
                new_population.individuals[0] = population.fittest()
                elitism_offset = 1
            # selection and crossover
            for i in range(elitism_offset, self.population_size):
                parent1 = self.selection(population)
                parent2 = self.selection(population)
                child = self.crossover(parent1, parent2)
                new_population.individuals[i] = child
            # mutation
            for i in range(elitism_offset, self.population_size):
                self.mutate(new_population.individuals[i])
            population = new_population
            if verbose:
                winner = population.fittest()
                print(gn + 1, winner, winner.distance)

        # return the result
        return population.fittest()

    def selection(self, population):
        # selects candidate route for crossover
        tournament = Population(self.mtx, self.tournament_size)
        for i in range(self.tournament_size):
            random_id = int(random.random() * self.population_size)
            tournament.individuals[i] = population.individuals[random_id]
        best = tournament.fittest()
        return best

    @staticmethod
    def crossover(parent1, parent2):
        child = Individual(dist_matrix=parent1.mtx,
                           order=[None for _ in range(parent1.size)])
        # get start and end sub-route positions for parent1's route
        start_pos = int(random.random() * parent1.size)
        end_pos = int(random.random() * parent1.size)
        # loop and add the sub-route from parent1 to our child
        for i in range(child.size):
            if start_pos < end_pos and start_pos < i < end_pos:
                child.set_place(i, parent1.order[i])
            elif start_pos > end_pos:
                if not (end_pos < i < start_pos):
                    child.set_place(i, parent1.order[i])
        # loop through parent2's route
        for i in range(parent2.size):
            # if the child doesn't have the city add it
            if parent2.order[i] not in child.order:
                for j in range(child.size):
                    # spare position found and add the city
                    if child.order[j] is None:
                        child.set_place(j, parent2.order[i])
                        break
        return child

    def mutate(self, individual):
        for pos1 in range(individual.size):
            if random.random() < self.mutation_rate:
                pos2 = int(individual.size * random.random())
                place1 = individual.order[pos1]
                place2 = individual.order[pos2]
                individual.set_place(pos2, place1)
                individual.set_place(pos1, place2)


'''
mtx = []
size = 10
for i in range(size):
    row = [0 if i == j else random.random() for j in range(size)]
    mtx.append(row)
mtx = np.array(mtx)

# mtx = [
#        [0, 2, 5, 2, 3],
#        [3, 0, 2, 5, 2],
#        [6, 2, 0, 9, 8],
#        [7, 3, 8, 0, 1],
#        [1, 9, 3, 4, 0]
#       ]

winner = GA(mtx=mtx).evolve(verbose=True)
print("\nSolution:\n", winner)
'''
