def is_safe(processes, avail, maxm, allot):
    num_processos = len(processes)
    num_tipos_processo = len(avail)

    need = [[0] * num_tipos_processo for _ in range(num_processos)]
    for i in range(num_processos):
        for j in range(num_tipos_processo):
            need[i][j] = maxm[i][j] - allot[i][j]

    finish = [False] * num_processos
    safe_seq = [0] * num_processos
    work = avail[:]

    count = 0
    while count < num_processos:
        found = False
        for p in range(num_processos):
            if not finish[p]:
                for j in range(num_tipos_processo):
                    if need[p][j] > work[j]:
                        break
                else:
                    for k in range(num_tipos_processo):
                        work[k] += allot[p][k]
                    safe_seq[count] = processes[p]
                    count += 1
                    finish[p] = True
                    found = True
        if not found:
            return False, []

    return True, safe_seq


def banker(processes, avail, maxm, allot):
    is_safe_state, safe_seq = is_safe(processes, avail, maxm, allot)
    if is_safe_state:
        print("Sistema está em estado seguro.")
        print("Sequência segura é:\n", safe_seq)
    else:
        print("Sistema não está em estado seguro.")


# Exemplo de uso seguro
processes = [0, 1, 2, 3, 4]
avail = [3, 3, 2]
maxm = [
    [7, 5, 3],
    [3, 2, 2],
    [9, 0, 2],
    [2, 2, 2],
    [4, 3, 3]
]
allot = [
    [0, 1, 0],
    [2, 0, 0],
    [3, 0, 2],
    [2, 1, 1],
    [0, 0, 2]
]
banker(processes, avail, maxm, allot)

#Seguro
processes = [1, 2, 3]
avail = [10]
maxm = [
    [9],
    [4],
    [7]
]
allot = [
    [3],
    [2],
    [2]
]

banker(processes, avail, maxm, allot)

#Seguro
processes = [1, 2, 3]
avail = [3]  
maxm = [
    [9],
    [4],
    [7]
]
allot = [
    [2],  
    [2],
    [2]
]

banker(processes, avail, maxm, allot)

#inseguro
processes = [0, 1, 2, 3, 4]
avail = [0, 3, 0]  # Recursos disponíveis insuficientes para atender aos pedidos
maxm = [
    [7, 5, 3],
    [3, 2, 2],
    [9, 0, 2],
    [2, 2, 2],
    [4, 3, 3]
]
allot = [
    [0, 1, 0],
    [2, 0, 0],
    [3, 0, 2],
    [2, 1, 1],
    [0, 0, 2]
]

banker(processes, avail, maxm, allot)
