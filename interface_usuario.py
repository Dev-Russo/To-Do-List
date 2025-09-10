from datetime import datetime

OPTION_1 = "1: Adicionar nova tarefa"
OPTION_2 = "2: Listar todas as tarefas"
OPTION_3 = "3: Marcar tarefa como concluída"
OPTION_4 = "4: Remover tarefa"
OPTION_5 = "5: Alterar tarefa"
OPTION_6 = "6: Sair"

PRIORIDADES = ["Baixa", "Média", "Alta"]

MAPEAMENTO_DE_PRIORIDADES = {
    "Baixa": 1,
    "Média": 2,
    "Alta": 3
}

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
        tarefas.sort(key=lambda x: MAPEAMENTO_DE_PRIORIDADES.get(x.get('prioridade', ''), 0), reverse=True)
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
