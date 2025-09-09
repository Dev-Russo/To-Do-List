import json

OPTION_1 = "1: Adicionar nova tarefa"
OPTION_2 = "2: Listar todas as tarefas"
OPTION_3 = "3: Marcar tarefa como concluída"
OPTION_4 = "4: Remover tarefa"
OPTION_5 = "5: Sair"

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
    print(OPTION_1)
    print(OPTION_2)
    print(OPTION_3)
    print(OPTION_4)
    print(OPTION_5)

def adicionar_tarefa(tarefas):
    descricao = input("Digite a descrição da tarefa: ")
    tarefa = {"descricao": descricao, "concluida": False}
    tarefas.append(tarefa)
    salvar_tarefas(tarefas)
    print(f"TAREFA '{descricao}' ADICIONADA COM SUCESSO!")

def listar_tarefas(tarefas): 
    print("LISTA DE TAREFAS:")
    if not tarefas:
        print("Nenhuma tarefa encontrada.")
        return
    for i, tarefa in enumerate(tarefas, start=1):
        status = "Concluída" if tarefa["concluida"] else "Pendente"
        print(f"{i}. {tarefa['descricao']} - {status}")
    salvar_tarefas(tarefas)

def marcar_concluida(tarefas):
    if tarefas:
        listar_tarefas(tarefas)
        try:
            index = int(input("Digite o número da tarefa que deseja marcar como concluída: ")) - 1
            if 0 <= index < len(tarefas):
                tarefas[index]["concluida"] = True
                print(f"TAREFA '{tarefas[index]['descricao']}' MARCADA COMO CONCLUÍDA!")
            else:
                print("Número inválido.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")
        salvar_tarefas(tarefas)

def remover_tarefa(tarefas):
    if tarefas:
        listar_tarefas(tarefas)
        try:
            index = int(input("Digite o número da tarefa que deseja remover: ")) - 1
            if 0 <= index < len(tarefas):
                tarefa_removida = tarefas.pop(index)
                print(f"TAREFA '{tarefa_removida['descricao']}' REMOVIDA COM SUCESSO!")
            else:
                print("Número inválido.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")
        salvar_tarefas(tarefas)

def sair():
    print("Saindo do programa. Até mais!")
    exit()

def resolution_option(N):
    print("\n")
    if N == 1:
        print("Adicionar nova tarefa")
        adicionar_tarefa(carregar_tarefas())
    elif N == 2:
        print("Listar todas as tarefas")
        listar_tarefas(carregar_tarefas())
    elif N == 3: 
        print("Marcar tarefa como concluída")
        marcar_concluida(carregar_tarefas())
    elif N == 4:
        print("Remover tarefa")
        remover_tarefa(carregar_tarefas())
    elif N == 5:
        sair()
    else:
        print("Opção inválida. Tente novamente.")
    
    
    
def main():
    while True:
        options()
        N = int(input())
        resolution_option(N)
                
    
if __name__ == "__main__":
    main()