class Processo:
    def __init__(self, pid, tempo_chegada, tempo_execucao):
        self.pid = pid
        self.tempo_chegada = tempo_chegada
        self.tempo_execucao = tempo_execucao
        self.tempo_restante = tempo_execucao
        self.tempo_inicio = -1
        self.tempo_conclusao = 0
        self.tempo_espera = 0
        self.tempo_resposta = 0
        self.tempo_vida = 0 


def escalonamento_rr(processos, quantum, tempo_troca_contexto=0):
    fila_prontos = []
    tempo_atual = 0
    processos_concluidos = []
    processos_restantes = processos[:]
    id_processo_executando = -1

    processos_restantes.sort(key=lambda x: x.tempo_chegada)

    while processos_restantes or fila_prontos:
        # Adiciona processos que chegaram à fila de prontos
        while processos_restantes and processos_restantes[0].tempo_chegada <= tempo_atual:
            processo = processos_restantes.pop(0)
            fila_prontos.append(processo)
            print(f"Tempo {tempo_atual}: Processo {processo.pid} chegou e entrou na fila.")

        if not fila_prontos:
            if processos_restantes:
                tempo_atual = processos_restantes[0].tempo_chegada
                print(f"Tempo {tempo_atual}: Fila vazia. Avançando para a chegada do próximo processo.")
            else:
                break

        processo_atual = fila_prontos.pop(0)

        if id_processo_executando != -1 and id_processo_executando != processo_atual.pid:
            tempo_atual += tempo_troca_contexto
            print(f"Tempo {tempo_atual}: Troca de contexto ({tempo_troca_contexto} unidades).")

        id_processo_executando = processo_atual.pid

        if processo_atual.tempo_inicio == -1:
            processo_atual.tempo_inicio = tempo_atual
            processo_atual.tempo_resposta = tempo_atual - processo_atual.tempo_chegada

        tempo_executado = min(quantum, processo_atual.tempo_restante)
        tempo_atual += tempo_executado
        processo_atual.tempo_restante -= tempo_executado
        print(f"Tempo {tempo_atual}: Processo {processo_atual.pid} executou por {tempo_executado} unidades (restante: {processo_atual.tempo_restante}).")

        if processo_atual.tempo_restante == 0:
            processo_atual.tempo_conclusao = tempo_atual
            processo_atual.tempo_espera = processo_atual.tempo_conclusao - processo_atual.tempo_chegada - processo_atual.tempo_execucao
            processo_atual.tempo_vida = processo_atual.tempo_conclusao - processo_atual.tempo_chegada # Calcula o tempo de vida
            processos_concluidos.append({
                "pid": processo_atual.pid,
                "tempo_chegada": processo_atual.tempo_chegada,
                "tempo_execucao": processo_atual.tempo_execucao,
                "tempo_inicio": processo_atual.tempo_inicio,
                "tempo_conclusao": processo_atual.tempo_conclusao,
                "tempo_espera": processo_atual.tempo_espera,
                "tempo_resposta": processo_atual.tempo_resposta,
                "tempo_vida": processo_atual.tempo_vida  # Adicionado: Tempo de vida
            })
            print(f"Tempo {tempo_atual}: Processo {processo_atual.pid} terminou.")

        else:
            # Adiciona processos que CHEGARAM DURANTE A EXECUÇÃO à fila ANTES de re-adicionar o processo atual.
            while processos_restantes and processos_restantes[0].tempo_chegada <= tempo_atual:
                processo = processos_restantes.pop(0)
                fila_prontos.append(processo)
                print(f"Tempo {tempo_atual}: Processo {processo.pid} chegou e entrou na fila.")

            fila_prontos.append(processo_atual) # Re-adiciona o processo atual ao final da fila.
            print(f"Tempo {tempo_atual}: Processo {processo_atual.pid} voltou para a fila.")

    return processos_concluidos


if __name__ == "__main__":
    processos = [
        Processo(1, 5, 10),
        Processo(2, 15, 30),
        Processo(3, 10, 20),
        Processo(4, 0, 40)
    ]
    quantum = 15
    tempo_troca_contexto = 4

    resultados = escalonamento_rr(processos, quantum, tempo_troca_contexto)

    print("\nResultados:")
    print("PID\tChegada\tExecução\tInício\tConclusão\tEspera\tResposta\tVida")  # Adicionado: Cabeçalho para Tempo de Vida
    for resultado in resultados:
        print(f"{resultado['pid']}\t{resultado['tempo_chegada']}\t{resultado['tempo_execucao']}\t\t{resultado['tempo_inicio']}\t{resultado['tempo_conclusao']}\t\t{resultado['tempo_espera']}\t{resultado['tempo_resposta']}\t\t{resultado['tempo_vida']}") # Adicionado: Impressão do tempo de vida

    tempo_medio_espera = sum(r['tempo_espera'] for r in resultados) / len(resultados)
    tempo_medio_resposta = sum(r['tempo_resposta'] for r in resultados) / len(resultados)
    tempo_medio_vida = sum(r['tempo_vida'] for r in resultados) / len(resultados)  # Adicionado: Cálculo do Tempo Médio de Vida
    tempo_total_conclusao = max(r['tempo_conclusao'] for r in resultados)

    print(f"\nTempo Médio de Espera: {tempo_medio_espera:.2f}")
    print(f"Tempo Médio de Resposta: {tempo_medio_resposta:.2f}")
    print(f"Tempo Médio de Vida: {tempo_medio_vida:.2f}") # Adicionado: Impressão do Tempo Médio de Vida
    print(f"Makespan (Tempo total de conclusão): {tempo_total_conclusao}")