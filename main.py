import os
import gerenciador_tarefas as gt
import gerenciador_arquivos as ga
import interface_usuario as iu
    
def main():
    lista_de_tarefas = []
    lista_de_tarefas = ga.carregar_tarefas()
    while True:
        iu.options()
        N = int(input())
        os.system('cls')
        gt.resolution_option(N, lista_de_tarefas)
    

if __name__ == "__main__":
    main()