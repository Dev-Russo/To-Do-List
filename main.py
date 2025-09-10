import os
import gerenciador_tarefas as gt
import gerenciador_arquivos as ga
import interface_usuario as iu
  
  
COMANDOS = {
    1: gt.adicionar_tarefa,
    2: iu.list_format,
    3: gt.marcar_concluida,
    4: gt.remover_tarefa,
    5: gt.update_tarefas,
    6: gt.sair_e_salvar
}  

def resolution_option(N, lista_de_tarefas):
    if N == 1:
        print("")
        print("Adicionar nova tarefa")
        adicionar_tarefa(lista_de_tarefas)
    elif N == 2:
        print("")
        print("Listar todas as tarefas")
        iu.list_format(lista_de_tarefas)
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
        sair_e_salvar()
    else:
        print("Opção inválida. Tente novamente.")

def main():
    lista_de_tarefas = []
    lista_de_tarefas = ga.carregar_tarefas()
    while True:
        iu.options()
        N = int(input())
        os.system('cls')
        resolution_option(N, lista_de_tarefas)
    

if __name__ == "__main__":
    main()