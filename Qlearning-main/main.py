import connection as cn
import numpy as np
from random import randint

# função que retorna a melhor ação para um estado
def best_action(curr_state):
    if np.random.random() < epsilon:
        return randint(0, 2)
    else:
        return np.argmax(matrix_utility[curr_state])
    
# carrega a matriz de utilidade e conecta ao servidor
matrix_utility = np.loadtxt('resultado.txt')
socket = cn.connect(2037)

# define o estado inicial e a recompensa
curr_state = 0
curr_reward = -14
actions = ["left", "right", "jump"]

# taxa de aprendizado, fator de desconto e taxa de exploracao
alpha = 0.01
gamma = 0.05
epsilon = 0

# Histórico de estados e penalidade para loops
# visited_states = []
# loop_penalty = -3.0
# loop_threshold = 5 

while True:
    # escolhe uma ação
    action = best_action(curr_state)
    print(f'Acao escolhida para o estado {curr_state}: {actions[action]}')

    # executa a ação e recebe o estado e a recompensa
    state, reward = cn.get_state_reward(socket, actions[action])
    state = int(state[2:], 2)
    next_state = state

    # Verifica se o estado foi visitado recentemente para penalizar loops
    # if curr_state in visited_states:
    #     print(f'Loop detectado no estado {curr_state}. Aplicando penalidade.')
    #     reward += loop_penalty

    # # Adiciona o estado atual ao histórico de estados visitados
    # visited_states.append(curr_state)
    # if len(visited_states) > loop_threshold:
    #     visited_states.pop(0)

    print(f'Valor anterior desta acao: {matrix_utility[curr_state][action]}')
    # atualiza a matriz de utilidade
    matrix_utility[curr_state][action] = matrix_utility[curr_state][action] + alpha * ((curr_reward + gamma * max(matrix_utility[next_state])) - matrix_utility[curr_state][action])
    print(f'Novo valor: {matrix_utility[curr_state][action]}')
    print()

    # atualiza o estado atual e a recompensa
    curr_state = next_state
    curr_reward = reward
    np.savetxt('resultado.txt', matrix_utility) # salva a matriz de utilidade

