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

def main():
    lista_de_tarefas = []
    lista_de_tarefas = ga.carregar_tarefas()
    while True:
        try:
            iu.options()
            N = int(input("Escolha uma opção: "))
            os.system('cls')

            if N in COMANDOS:
                funcao_escolhida = COMANDOS[N]
                if N == 6: 
                    funcao_escolhida(lista_de_tarefas)
                    break 
                else:
                    funcao_escolhida(lista_de_tarefas)
            else:
                print("Opção inválida. Por favor, escolha um número do menu.")

        except ValueError:
            print("Entrada inválida. Por favor, digite um NÚMERO.")

if __name__ == "__main__":
    main()