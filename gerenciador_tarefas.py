import os
import json
import interface_usuario as iu
import gerenciador_arquivos as ga


def adicionar_tarefa(tarefas):
    print("Digite 2 para voltar ao menu")
    descricao = input("Digite a descrição da tarefa: ")
    if descricao != "2":
        tarefa = {"descricao": descricao, "concluida": False}
        prioridade = iu.definir_prioridades()
        data_termino = iu.definir_data_hora()
        if data_termino:
            tarefa["data_termino"] = data_termino.strftime("%d/%m/%Y")
        if prioridade:
            tarefa["prioridade"] = prioridade
        tarefas.append(tarefa)
        print(f"TAREFA '{descricao}' ADICIONADA COM SUCESSO!")
    else:
        pass
    
def remover_tarefa(tarefas):
    if tarefas:
        iu.listar_tarefas(tarefas)
        print("Digite o número da tarefa que deseja remover: ")
        tarefa_selecionada = iu.selecionar_tarefas(tarefas)
        if tarefa_selecionada is not None:
            tarefa_excluida = tarefas.pop(tarefa_selecionada)
            print(f"TAREFA '{tarefa_excluida['descricao']}' REMOVIDA COM SUCESSO!")

def marcar_concluida(tarefas):
    if tarefas:
        iu.listar_tarefas(tarefas)
        print("Digite o número da tarefa que deseja marcar como concluída: ")
        tarefa_selecionada = iu.selecionar_tarefas(tarefas)
        if tarefa_selecionada is not None:
            tarefas[tarefa_selecionada]["concluida"] = True
            print(f"TAREFA '{tarefas[tarefa_selecionada]['descricao']}' MARCADA COMO CONCLUÍDA!")
   
##Update de Tarefas
def update_tarefas(tarefas):
    if tarefas:
        iu.listar_tarefas(tarefas)
        print("Selecione a Terefa que deseja editar: ")
        tarefa_selecionada = iu.selecionar_tarefas(tarefas)
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
                    nova_prioridade = iu.definir_prioridades() 
                    if nova_prioridade:
                        tarefas[tarefa_selecionada]['prioridade'] = nova_prioridade
                        print("Prioridade atualizada!")

                elif escolha == '3':
                    nova_data = iu.definir_data_hora() 
                    if nova_data:
                        tarefas[tarefa_selecionada]['data_termino'] = nova_data.strftime("%d/%m/%Y")
                        print("Data de término atualizada!")
                
                elif escolha == '4':
                    print(f"\nTAREFA '{tarefas[tarefa_selecionada]['descricao']}' ATUALIZADA COM SUCESSO!")
                    break
                
                else:
                    print("Opção inválida. Tente novamente.")    


def sair_e_salvar(tarefas):
    ga.salvar_tarefas(tarefas)
    print("Saindo do programa. Até mais!")
    exit()

