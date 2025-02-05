def is_safe_state(available, allocation, max_demand, need):
    num_processes = len(allocation)
    num_resources = len(available)

    work = available[:]
    finish = [False] * num_processes

    while True:
        found = False
        for i in range(num_processes):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(num_resources)):
                for j in range(num_resources):
                    work[j] += allocation[i][j]
                finish[i] = True
                found = True

        if not found:
            break

    return all(finish)

def banker_algorithm(available, allocation, max_demand):
    num_processes = len(allocation)
    num_resources = len(available)

    need = [[max_demand[i][j] - allocation[i][j] for j in range(num_resources)] for i in range(num_processes)]

    print("Estado inicial:")
    print("Disponível:", available)
    print("Alocação:", allocation)
    print("Máxima demanda:", max_demand)
    print("Necessidade:", need)

    if is_safe_state(available, allocation, max_demand, need):
        print("O sistema está em um estado seguro.")
    else:
        print("O sistema está em um estado inseguro.")

def main():
    num_processes = int(input("Digite o número de processos: "))
    num_resources = int(input("Digite o número de tipos de recursos: "))

    available = list(map(int, input(f"Digite a quantidade de cada um dos {num_resources} recursos disponíveis, separados por espaço: ").split()))

    allocation = []
    for i in range(num_processes):
        allocation.append(list(map(int, input(f"Digite a alocação atual dos {num_resources} recursos para o processo {i}, separados por espaço: ").split())))

    max_demand = []
    for i in range(num_processes):
        max_demand.append(list(map(int, input(f"Digite a demanda máxima dos {num_resources} recursos para o processo {i}, separados por espaço: ").split())))

    banker_algorithm(available, allocation, max_demand)

if __name__ == "__main__":
    main()
