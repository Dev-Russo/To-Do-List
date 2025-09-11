# Mensagens do sistema
MENSAGENS = {
    # Mensagens de sucesso
    'tarefa_adicionada': "TAREFA '{}' ADICIONADA COM SUCESSO!",
    'tarefa_removida': "TAREFA '{}' REMOVIDA COM SUCESSO!",
    'tarefa_concluida': "TAREFA '{}' MARCADA COMO CONCLUÍDA!",
    'tarefa_atualizada': "TAREFA '{}' ATUALIZADA COM SUCESSO!",
    
    # Mensagens de erro
    'opcao_invalida': "Opção inválida. Tente novamente.",
    'numero_invalido': "Número inválido.",
    'entrada_invalida': "Entrada inválida. Por favor, digite um número.",
    'formato_data_invalido': "Formato de data inválido. Use dd/mm/aaaa.",
    'nenhuma_tarefa': "Nenhuma tarefa encontrada.",
    
    # Prompts de entrada
    'prompt_descricao': "Digite a descrição da tarefa: ",
    'prompt_prioridade': "Selecione a prioridade (1-3): ",
    'prompt_data': "Defina a data de termino da atividade (dd/mm/aaaa): ",
    'prompt_opcao': "Escolha uma opção: ",
    
    # Mensagens de navegação
    'voltar_menu': "Digite 2 para voltar ao menu",
    'saindo_programa': "Saindo do programa. Até mais!",
}

# Opções do menu principal
OPCOES_MENU = {
    1: "Adicionar nova tarefa",
    2: "Listar todas as tarefas", 
    3: "Marcar tarefa como concluída",
    4: "Remover tarefa",
    5: "Alterar tarefa",
    6: "Sair"
}

# Opções de listagem
OPCOES_LISTAGEM = {
    1: "Ordem Alfabética",
    2: "Por Prioridade", 
    3: "Por Status (Concluída/Pendente)",
    4: "Data de Término"
}

# Opções de edição de tarefa
OPCOES_EDICAO = {
    1: "Descrição",
    2: "Prioridade", 
    3: "Data de Término",
    4: "Salvar e voltar ao menu principal"
}

# Prioridades disponíveis
PRIORIDADES = ["Baixa", "Média", "Alta"]

MAPEAMENTO_PRIORIDADES = {
    "Baixa": 1,
    "Média": 2, 
    "Alta": 3
}

# Configurações do arquivo
NOME_ARQUIVO = "tarefas.json"
ENCODING = "utf-8"

# Formatos
FORMATO_DATA = "%d/%m/%Y"