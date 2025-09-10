from datetime import datetime
import json
import os

OPTION_1 = "1: Adicionar nova tarefa"
OPTION_2 = "2: Listar todas as tarefas"
OPTION_3 = "3: Marcar tarefa como concluída"
OPTION_4 = "4: Remover tarefa"
OPTION_5 = "5: Alterar tarefa"
OPTION_6 = "6: Sair"

PRIORIDADES = ["Baixa", "Média", "Alta"]

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
    
def definir_prioridades():
    print("Prioridades disponíveis:")
    for i, prioridade in enumerate(PRIORIDADES, start=1):
        print(f"{i}. {prioridade}")
    index = int(input("Selecione a prioridade (1-3): ")) - 1
    if 0 <= index < len(PRIORIDADES):
        return PRIORIDADES[index]
    
def definir_data_hora():
    print("Defina a data de termino da atividade (dd/mm/aaaa:): ")
    data_input = input()
    try:
        data_termino = datetime.strptime(data_input, "%d/%m/%Y")
        return data_termino
    except ValueError:
        print("Formato de data inválido. Use dd/mm/aaaa.")
        return None

def adicionar_tarefa(tarefas):
    print("Digite 2 para voltar ao menu")
    descricao = input("Digite a descrição da tarefa: ")
    if descricao != "2":
        tarefa = {"descricao": descricao, "concluida": False}
        prioridade = definir_prioridades()
        data_termino = definir_data_hora()
        if data_termino:
            tarefa["data_termino"] = data_termino.strftime("%d/%m/%Y")
        if prioridade:
            tarefa["prioridade"] = prioridade
        tarefas.append(tarefa)
        print(f"TAREFA '{descricao}' ADICIONADA COM SUCESSO!")
    else:
        pass
    
def list_format(tarefas):
    print("Como você gostaria de listar as tarefas?")
    print("1: Ordem Alfabética")
    print("2: Por Prioridade")
    print("3: Por Status (Concluída/Pendente)")
    print("4: DateTime de Término")
    type = int(input())
    if type == 1:
        tarefas.sort(key=lambda x: x['descricao'])
    elif type == 2: 
        tarefas.sort(key=lambda x: x['prioridade'])
    elif type == 3:
        tarefas.sort(key=lambda x: x['concluida'])
    elif type == 4:
        tarefas.sort(key=lambda x: datetime.strptime(x['data_termino'], "%d/%m/%Y") if 'data_termino' in x else datetime.max)
    else:
        print("Opção inválida. Listando na ordem original.")
    listar_tarefas(tarefas)

def listar_tarefas(tarefas):
    print("LISTA DE TAREFAS:")
    if not tarefas:
        print("Nenhuma tarefa encontrada.")
        return
    for i, tarefa in enumerate(tarefas, start=1):
        status = "Concluída" if tarefa["concluida"] else "Pendente"
        prioridade = tarefa.get("prioridade", "Sem prioridade")
        data_termino = tarefa.get("data_termino", "Sem data de término")
        print(f"{i}. {tarefa['descricao']} - {prioridade} - {status} - {data_termino} ")

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
            print("Selecione o que deseja alterar: ")
            while True:
                tarefa_atual = tarefas[tarefa_selecionada]
                print("\n--- Editando Tarefa ---")
                print(f"Descrição: {tarefa_atual.get('descricao', 'N/D')}")
                print(f"Prioridade: {tarefa_atual.get('prioridade', 'N/D')}")
                print(f"Data de Término: {tarefa_atual.get('data_termino', 'N/D')}")
                print("-------------------------")

                print("O que deseja alterar?")
                escolha = input("1: Descrição\n2: Prioridade\n3: Data de Término\n4: Salvar e voltar ao menu principal\nSua escolha: ")

                if escolha == '1':
                    nova_descricao = input("Digite a nova descrição: ")
                    tarefas[tarefa_selecionada]['descricao'] = nova_descricao
                    print("Descrição atualizada!")

                elif escolha == '2':
                    nova_prioridade = definir_prioridades() 
                    if nova_prioridade:
                        tarefas[tarefa_selecionada]['prioridade'] = nova_prioridade
                        print("Prioridade atualizada!")

                elif escolha == '3':
                    nova_data = definir_data_hora() 
                    if nova_data:
                        tarefas[tarefa_selecionada]['data_termino'] = nova_data.strftime("%d/%m/%Y")
                        print("Data de término atualizada!")
                
                elif escolha == '4':
                    print(f"\nTAREFA '{tarefas[tarefa_selecionada]['descricao']}' ATUALIZADA COM SUCESSO!")
                    break
                
                else:
                    print("Opção inválida. Tente novamente.")
                
            
        
        
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
        list_format(lista_de_tarefas)
    elif N == 3:
        print("")
        print("Marcar tarefa como concluída")
        marcar_concluida(lista_de_tarefas)
    elif N == 4:
        print("")
        print("Remover tarefa")
        remover_tarefa(lista_de_tarefas)
    elif N == 5:
        print("")
        print("Alterar Descricao da Tarefa")
        update_tarefas(lista_de_tarefas)
    elif N == 6:
        salvar_tarefas(lista_de_tarefas)
        sair()
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