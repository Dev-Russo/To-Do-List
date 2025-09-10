import json

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