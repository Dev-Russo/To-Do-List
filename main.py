import json
import os

OPTION_1 = "1: Adicionar nova tarefa"
OPTION_2 = "2: Listar todas as tarefas"
OPTION_3 = "3: Marcar tarefa como concluída"
OPTION_4 = "4: Remover tarefa"
OPTION_5 = "5: Alterar tarefa"
OPTION_6 = "6: Sair"

NAME_ARQUIVO = "tarefas.json"

def carregar_tarefas():
    try:
        with open(NAME_ARQUIVO, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []
    
def salvar_tarefas(tarefas):
    with open(NAME_ARQUIVO, 'w') as file:
        json.dump(tarefas, file, indent=4)

def options():
    print(" ")
    print(OPTION_1)
    print(OPTION_2)
    print(OPTION_3)
    print(OPTION_4)
    print(OPTION_5)
    print(OPTION_6)

def adicionar_tarefa(tarefas):
    print("Digite 2 para voltar ao menu")
    descricao = input("Digite a descrição da tarefa: ")
    if descricao != "2":
        tarefa = {"descricao": descricao, "concluida": False}
        tarefas.append(tarefa)
        print(f"TAREFA '{descricao}' ADICIONADA COM SUCESSO!")
    else:
        pass

def listar_tarefas(tarefas):
    print("LISTA DE TAREFAS:")
    if not tarefas:
        print("Nenhuma tarefa encontrada.")
        return
    for i, tarefa in enumerate(tarefas, start=1):
        status = "Concluída" if tarefa["concluida"] else "Pendente"
        print(f"{i}. {tarefa['descricao']} - {status}")

def selecionar_tarefas(tarefas):
    try:
        index = int(input()) - 1
        if 0 <= index < len(tarefas):
            return index
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")


def marcar_concluida(tarefas):
    if tarefas:
        listar_tarefas(tarefas)
        print("Digite o número da tarefa que deseja marcar como concluída: ")
        tarefa_selecionada = selecionar_tarefas(tarefas)
        if tarefa_selecionada is not None:
            tarefas[tarefa_selecionada]["concluida"] = True
            print(f"TAREFA '{tarefas[tarefa_selecionada]['descricao']}' MARCADA COMO CONCLUÍDA!")
        

def remover_tarefa(tarefas):
    if tarefas:
        listar_tarefas(tarefas)
        print("Digite o número da tarefa que deseja remover: ")
        tarefa_selecionada = selecionar_tarefas(tarefas)
        if tarefa_selecionada is not None:
            tarefa_excluida = tarefas.pop(tarefa_selecionada)
            print(f"TAREFA '{tarefa_excluida['descricao']}' REMOVIDA COM SUCESSO!")


##Update de Tarefas
def update_tarefas(tarefas):
    if tarefas:
        listar_tarefas(tarefas)
        print("Selecione a Terefa que deseja editar: ")
        tarefa_selecionada = selecionar_tarefas(tarefas)
        if tarefa_selecionada is not None:
            print("De a nova descrição para sua tarefa: ")
            nova_descricao = input()
            tarefas[tarefa_selecionada]['descricao'] = nova_descricao

def sair():
    print("Saindo do programa. Até mais!")
    exit()

def resolution_option(N, lista_de_tarefas):
    if N == 1:
        print("")
        print("Adicionar nova tarefa")
        adicionar_tarefa(lista_de_tarefas)
    elif N == 2:
        print("")
        print("Listar todas as tarefas")
        listar_tarefas(lista_de_tarefas)
    elif N == 3:
        print("")
        print("Marcar tarefa como concluída")
        marcar_concluida(lista_de_tarefas)
    elif N == 4:
        print("")
        print("Remover tarefa")
        remover_tarefa(lista_de_tarefas)
    elif N == 6:
        salvar_tarefas(lista_de_tarefas)
        sair()
    elif N == 5:
        print("")
        print("Alterar Descricao da Tarefa")
        update_tarefas(lista_de_tarefas)
    else:
        print("Opção inválida. Tente novamente.")
    
def main():
    lista_de_tarefas = []
    lista_de_tarefas = carregar_tarefas()
    while True:
        options()
        N = int(input())
        os.system('cls')
        resolution_option(N, lista_de_tarefas)
    

if __name__ == "__main__":
    main()