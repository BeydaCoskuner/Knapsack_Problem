import random
import time
import matplotlib.pyplot as plt

def dynamic_programming(weights, values, capacity):

    n = len(weights)

    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):

        for w in range(1, capacity + 1):

            if weights[i - 1] <= w:

                dp[i][w] = max(
                    values[i - 1]
                    + dp[i - 1][w - weights[i - 1]],

                    dp[i - 1][w]
                )

            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]

def genetic_algorithm(weights, values, capacity):

    n = len(weights)

    population_size = 20
    generations = 50
    mutation_rate = 0.1

    def fitness(chromosome):

        total_weight = 0
        total_value = 0

        for i in range(n):

            if chromosome[i] == 1:

                total_weight += weights[i]
                total_value += values[i]

        if total_weight > capacity:
            return 0

        return total_value

    population = []

    for _ in range(population_size):

        chromosome = [
            random.randint(0, 1)
            for _ in range(n)
        ]

        population.append(chromosome)

    for _ in range(generations):

        population = sorted(
            population,
            key=fitness,
            reverse=True
        )

        new_population = population[:2]

        while len(new_population) < population_size:

            parent1 = random.choice(population[:5])
            parent2 = random.choice(population[:5])

            crossover_point = random.randint(1, n - 1)

            child = (
                parent1[:crossover_point]
                + parent2[crossover_point:]
            )

            if random.random() < mutation_rate:

                mutation_index = random.randint(0, n - 1)

                child[mutation_index] = (
                    1 - child[mutation_index]
                )

            new_population.append(child)

        population = new_population

    best_solution = max(population, key=fitness)

    return fitness(best_solution)

sizes = [100, 1000, 10000]

dp_times = []
ga_times = []

accuracy_gaps = []

for n in sizes:

    print(f"\nTEST BAŞLADI -> N = {n}")

    weights = [
        random.randint(1, 20)
        for _ in range(n)
    ]

    values = [
        random.randint(10, 100)
        for _ in range(n)
    ]

    capacity = n*5

    # DP süre ölçümü

    start = time.time()

    dp_result = dynamic_programming(
        weights,
        values,
        capacity
    )

    dp_time = time.time() - start


    # GA süre ölçümü
    start = time.time()

    ga_result = genetic_algorithm(
        weights,
        values,
        capacity
    )

    ga_time = time.time() - start

    # Accuracy Gap

    gap = (
        (dp_result - ga_result)
        / dp_result
    ) * 100

    # Listelere ekle

    dp_times.append(dp_time)
    ga_times.append(ga_time)

    accuracy_gaps.append(gap)

    # Yazdır

    print("DP Sonuç:", dp_result)
    print("GA Sonuç:", ga_result)

    print("DP Süre:", dp_time)
    print("GA Süre:", ga_time)

    print("Accuracy Gap:", gap)


plt.figure(figsize=(8, 5))

plt.plot(
    sizes,
    dp_times,
    marker='o',
    label='Dynamic Programming'
)

# Süre Karşılaştırma
plt.figure(figsize=(10, 6))

plt.plot(
    sizes,
    dp_times,
    marker='o',
    linewidth=2,
    label='Dynamic Programming'
)

plt.plot(
    sizes,
    ga_times,
    marker='s',
    linewidth=2,
    label='Genetic Algorithm'
)

plt.xlabel("Problem Size (N)", fontsize=12)

plt.ylabel("Runtime (seconds)", fontsize=12)

plt.title(
    "Runtime Comparison of DP and GA",
    fontsize=14
)

plt.legend()

plt.grid(True)

plt.savefig(
    "graphs/runtime_comparison.png",
    dpi=300
)

plt.show()

# Accuracy Gap Grafiği
plt.figure(figsize=(10, 6))

plt.plot(
    sizes,
    accuracy_gaps,
    marker='o',
    linewidth=2
)

plt.xlabel("Problem Size (N)", fontsize=12)

plt.ylabel("Accuracy Gap (%)", fontsize=12)

plt.title(
    "Accuracy Gap of Genetic Algorithm",
    fontsize=14
)

plt.grid(True)

plt.savefig(
    "graphs/accuracy_gap.png",
    dpi=300
)

plt.show()
