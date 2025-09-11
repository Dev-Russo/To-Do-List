import os
from tarefa import Tarefa
from constantes import MENSAGENS, OPCOES_EDICAO
import interface_usuario as iu
import gerenciador_arquivos as ga

def adicionar_tarefa(lista_tarefas):
    """Adiciona uma nova tarefa à lista"""
    print(MENSAGENS['voltar_menu'])
    descricao = input(MENSAGENS['prompt_descricao'])
    
    if descricao == "2":
        return
    
    prioridade = iu.definir_prioridades()
    data_termino = iu.definir_data_hora()
    
    # Cria nova tarefa usando a classe
    nova_tarefa = Tarefa(descricao, prioridade, data_termino)
    lista_tarefas.append(nova_tarefa.to_dict())  # Converte para dict para compatibilidade
    
    print(MENSAGENS['tarefa_adicionada'].format(descricao))

def remover_tarefa(lista_tarefas):
    """Remove uma tarefa da lista"""
    if not lista_tarefas:
        print(MENSAGENS['nenhuma_tarefa'])
        return
    
    iu.listar_tarefas(lista_tarefas)
    print("Digite o número da tarefa que deseja remover: ")
    
    indice = iu.selecionar_tarefas(lista_tarefas)
    if indice is not None:
        tarefa_removida = lista_tarefas.pop(indice)
        print(MENSAGENS['tarefa_removida'].format(tarefa_removida['descricao']))

def marcar_concluida(lista_tarefas):
    """Marca uma tarefa como concluída"""
    if not lista_tarefas:
        print(MENSAGENS['nenhuma_tarefa'])
        return
    
    iu.listar_tarefas(lista_tarefas)
    print("Digite o número da tarefa que deseja marcar como concluída: ")
    
    indice = iu.selecionar_tarefas(lista_tarefas)
    if indice is not None:
        # Cria objeto Tarefa temporário para usar o método
        tarefa_obj = Tarefa.from_dict(lista_tarefas[indice])
        tarefa_obj.marcar_concluida()
        
        # Atualiza o dicionário na lista
        lista_tarefas[indice] = tarefa_obj.to_dict()
        print(MENSAGENS['tarefa_concluida'].format(tarefa_obj.descricao))

def update_tarefas(lista_tarefas):
    """Atualiza uma tarefa existente usando menu estruturado"""
    if not lista_tarefas:
        print(MENSAGENS['nenhuma_tarefa'])
        return
    
    iu.listar_tarefas(lista_tarefas)
    print("Selecione a tarefa que deseja editar: ")
    
    indice = iu.selecionar_tarefas(lista_tarefas)
    if indice is None:
        return
    
    # Cria objeto Tarefa para facilitar a edição
    tarefa_obj = Tarefa.from_dict(lista_tarefas[indice])
    
    while True:
        print(f"\n--- Editando Tarefa ---")
        print(f"Descrição: {tarefa_obj.descricao}")
        print(f"Prioridade: {tarefa_obj.prioridade}")
        print(f"Data de Término: {tarefa_obj.data_termino}")
        print("-" * 25)
        
        print("O que deseja alterar?")
        for num, opcao in OPCOES_EDICAO.items():
            print(f"{num}: {opcao}")
        
        try:
            escolha = int(input("Sua escolha: "))
            
            if escolha == 1:
                nova_descricao = input("Digite a nova descrição: ")
                tarefa_obj.alterar_descricao(nova_descricao)
                print("Descrição atualizada!")
            
            elif escolha == 2:
                nova_prioridade = iu.definir_prioridades()
                if nova_prioridade:
                    tarefa_obj.alterar_prioridade(nova_prioridade)
                    print("Prioridade atualizada!")
            
            elif escolha == 3:
                nova_data = iu.definir_data_hora()
                if nova_data:
                    tarefa_obj.alterar_data_termino(nova_data)
                    print("Data de término atualizada!")
            
            elif escolha == 4:
                # Salva as alterações de volta na lista
                lista_tarefas[indice] = tarefa_obj.to_dict()
                print(MENSAGENS['tarefa_atualizada'].format(tarefa_obj.descricao))
                break
            
            else:
                print(MENSAGENS['opcao_invalida'])
        
        except ValueError:
            print(MENSAGENS['entrada_invalida'])

def sair_e_salvar(lista_tarefas):
    """Salva as tarefas e sai do programa"""
    ga.salvar_tarefas(lista_tarefas)
    print(MENSAGENS['saindo_programa'])