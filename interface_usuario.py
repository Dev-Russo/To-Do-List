from datetime import datetime
from constantes import (
    OPCOES_MENU, OPCOES_LISTAGEM, PRIORIDADES, 
    MAPEAMENTO_PRIORIDADES, MENSAGENS, FORMATO_DATA
)

def mostrar_menu():
    """Exibe o menu principal usando as constantes"""
    print("\n" + "="*40)
    print("    GERENCIADOR DE TAREFAS")
    print("="*40)
    
    for numero, opcao in OPCOES_MENU.items():
        print(f"{numero}: {opcao}")
    print("="*40)

def definir_prioridades():
    """Define prioridade com melhor validação e usando constantes"""
    while True:
        print("\nPrioridades disponíveis:")
        for i, prioridade in enumerate(PRIORIDADES, start=1):
            print(f"  {i}. {prioridade}")
        
        try:
            escolha = input(MENSAGENS['prompt_prioridade'])
            if escolha.strip() == "":  # Permite pular a prioridade
                return None
            
            index = int(escolha) - 1
            if 0 <= index < len(PRIORIDADES):
                return PRIORIDADES[index]
            else:
                print(f"Digite um número entre 1 e {len(PRIORIDADES)}.")
        
        except ValueError:
            print(MENSAGENS['entrada_invalida'])

def definir_data_hora():
    """Define data com melhor validação usando constantes"""
    while True:
        print(f"\n{MENSAGENS['prompt_data']}")
        print("(Deixe em branco para pular)")
        
        data_input = input().strip()
        
        if not data_input:  # Permite pular a data
            return None
        
        try:
            data_termino = datetime.strptime(data_input, FORMATO_DATA)
            
            # Verifica se a data não é no passado
            if data_termino.date() < datetime.now().date():
                print("⚠️  A data não pode ser no passado. Tente novamente.")
                continue
            
            return data_termino
        
        except ValueError:
            print(MENSAGENS['formato_data_invalido'])
            print("Exemplo: 25/12/2024")

def escolher_formato_listagem():
    """Escolhe como listar as tarefas usando constantes"""
    print("\nComo você gostaria de listar as tarefas?")
    
    for numero, opcao in OPCOES_LISTAGEM.items():
        print(f"  {numero}: {opcao}")
    
    while True:
        try:
            escolha = int(input("\nSua escolha: "))
            if escolha in OPCOES_LISTAGEM:
                return escolha
            else:
                print(MENSAGENS['opcao_invalida'])
        except ValueError:
            print(MENSAGENS['entrada_invalida'])

def listar_tarefas_formatadas(lista_tarefas):
    """Lista tarefas com melhor formatação"""
    if not lista_tarefas:
        print(f"\n📝 {MENSAGENS['nenhuma_tarefa']}")
        return
    
    print(f"\n{'='*60}")
    print(f"{'LISTA DE TAREFAS':^60}")
    print(f"{'='*60}")
    
    for i, tarefa in enumerate(lista_tarefas, start=1):
        # Ícones para status
        icone_status = "✅" if tarefa["concluida"] else "⏳"
        
        # Formatação de prioridade com cores (simuladas com símbolos)
        prioridade = tarefa.get("prioridade", "Sem prioridade")
        if prioridade == "Alta":
            prioridade = "🔴 Alta"
        elif prioridade == "Média":
            prioridade = "🟡 Média"
        elif prioridade == "Baixa":
            prioridade = "🟢 Baixa"
        
        status = "Concluída" if tarefa["concluida"] else "Pendente"
        data_termino = tarefa.get("data_termino", "Sem data")
        
        print(f"{i:2d}. {icone_status} {tarefa['descricao'][:30]:<30} | {prioridade:<10} | {data_termino}")
    
    print("="*60)

def aplicar_ordenacao(lista_tarefas, tipo_ordenacao):
    """Aplica ordenação baseada na escolha do usuário"""
    if tipo_ordenacao == 1:  # Alfabética
        return sorted(lista_tarefas, key=lambda x: x['descricao'].lower())
    
    elif tipo_ordenacao == 2:  # Por prioridade
        return sorted(
            lista_tarefas, 
            key=lambda x: MAPEAMENTO_PRIORIDADES.get(x.get('prioridade', ''), 0), 
            reverse=True
        )
    
    elif tipo_ordenacao == 3:  # Por status
        return sorted(lista_tarefas, key=lambda x: x['concluida'])
    
    elif tipo_ordenacao == 4:  # Por data
        def ordenar_por_data(tarefa):
            data_str = tarefa.get('data_termino')
            if data_str and data_str != "Sem data de término":
                try:
                    return datetime.strptime(data_str, FORMATO_DATA)
                except ValueError:
                    pass
            return datetime.max  # Tarefas sem data vão para o final
        
        return sorted(lista_tarefas, key=ordenar_por_data)
    
    return lista_tarefas

def list_format(lista_tarefas):
    """Função principal para listagem formatada"""
    if not lista_tarefas:
        print(f"\n📝 {MENSAGENS['nenhuma_tarefa']}")
        return
    
    tipo_ordenacao = escolher_formato_listagem()
    tarefas_ordenadas = aplicar_ordenacao(lista_tarefas, tipo_ordenacao)
    listar_tarefas_formatadas(tarefas_ordenadas)

def selecionar_tarefas(lista_tarefas):
    """Seleciona uma tarefa com melhor validação"""
    if not lista_tarefas:
        return None
    
    while True:
        try:
            entrada = input("\nDigite o número da tarefa: ").strip()
            if not entrada:
                print("Por favor, digite um número.")
                continue
            
            index = int(entrada) - 1
            if 0 <= index < len(lista_tarefas):
                return index
            else:
                print(f"Digite um número entre 1 e {len(lista_tarefas)}.")
        
        except ValueError:
            print(MENSAGENS['entrada_invalida'])
        
        # Opção para cancelar
        cancelar = input("Digite 'c' para cancelar ou Enter para tentar novamente: ").strip().lower()
        if cancelar == 'c':
            return None

# Função de compatibilidade (mantém a interface antiga funcionando)
def options():
    """Função para compatibilidade com o código antigo"""
    mostrar_menu()

def listar_tarefas(lista_tarefas):
    """Função para compatibilidade com o código antigo"""
    listar_tarefas_formatadas(lista_tarefas)