import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import json
import os

class GerenciadorTarefasGUI:
    def __init__(self, root):
        self.root = root
        self.nome_arquivo = "tarefas.json"
        self.tarefas = self.carregar_tarefas()
        
        # Cores e estilo (definir ANTES de configurar janela)
        self.cores = {
            'bg_primary': '#f8f9fa',
            'bg_secondary': '#ffffff', 
            'accent': '#007bff',
            'accent_hover': '#0056b3',
            'success': '#28a745',
            'danger': "#000000",
            'warning': '#ffc107',
            'text_primary': '#212529',
            'text_secondary': '#6c757d',
            'border': '#dee2e6'
        }
        
        # Configuração da janela principal
        self.configurar_janela()
        self.configurar_estilo()
        self.criar_interface()
        self.atualizar_lista()
    
    def configurar_janela(self):
        """Configura a janela principal"""
        self.root.title("Gerenciador de Tarefas")
        self.root.geometry("900x600")
        self.root.configure(bg=self.cores['bg_primary'])
        
        # Centralizar janela na tela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"900x600+{x}+{y}")
        
        # Impedir redimensionamento muito pequeno
        self.root.minsize(700, 500)
    
    def configurar_estilo(self):
        """Configura estilos personalizados"""
        style = ttk.Style()
        
        # Estilo para botões
        style.configure('Custom.TButton',
                       padding=(20, 10),
                       font=('Segoe UI', 10),
                       borderwidth=1,
                       focuscolor='none')
        
        # Estilo para botão primário
        style.configure('Primary.TButton',
                       padding=(20, 10),
                       font=('Segoe UI', 10, 'bold'))
        
        # Estilo para labels de título
        style.configure('Title.TLabel',
                       font=('Segoe UI', 16, 'bold'),
                       background=self.cores['bg_primary'],
                       foreground=self.cores['text_primary'])
        
        # Estilo para treeview
        style.configure('Custom.Treeview',
                       font=('Segoe UI', 10),
                       rowheight=35,
                       fieldbackground=self.cores['bg_secondary'])
        
        style.configure('Custom.Treeview.Heading',
                       font=('Segoe UI', 11, 'bold'),
                       padding=(10, 10))
    
    def criar_interface(self):
        """Cria a interface principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Configurar grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="Minhas Tarefas", style='Title.TLabel')
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        # Frame esquerdo - Botões
        frame_botoes = ttk.Frame(main_frame, padding="10")
        frame_botoes.grid(row=1, column=0, sticky="ns", padx=(0, 10))
        
        # Botões
        self.criar_botoes(frame_botoes)
        
        # Frame direito - Lista de tarefas
        frame_lista = ttk.Frame(main_frame, padding="10")
        frame_lista.grid(row=1, column=1, sticky="nsew")
        frame_lista.grid_rowconfigure(0, weight=1)
        frame_lista.grid_columnconfigure(0, weight=1)
        
        # Treeview para lista de tarefas
        self.criar_treeview(frame_lista)
        
        # Frame inferior - Estatísticas
        frame_stats = ttk.Frame(main_frame, padding="10")
        frame_stats.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        self.criar_estatisticas(frame_stats)
    
    def criar_botoes(self, parent):
        """Cria os botões de ação"""
        botoes = [
            ("➕ Adicionar Tarefa", self.adicionar_tarefa, 'Primary.TButton'),
            ("✏️ Editar Tarefa", self.editar_tarefa, 'Custom.TButton'),
            ("✅ Marcar Concluída", self.marcar_concluida, 'Custom.TButton'),
            ("❌ Remover Tarefa", self.remover_tarefa, 'Custom.TButton'),
            ("🔄 Atualizar Lista", self.atualizar_lista, 'Custom.TButton'),
        ]
        
        for i, (texto, comando, estilo) in enumerate(botoes):
            btn = ttk.Button(parent, text=texto, command=comando, style=estilo, width=18)
            btn.grid(row=i, column=0, pady=5, sticky="ew")
        
        # Separador
        separator = ttk.Separator(parent, orient='horizontal')
        separator.grid(row=len(botoes), column=0, sticky="ew", pady=15)
        
        # Filtros
        ttk.Label(parent, text="🔍 Filtros:", font=('Segoe UI', 10, 'bold')).grid(row=len(botoes)+1, column=0, sticky="w", pady=(0, 5))
        
        ttk.Button(parent, text="📋 Todas", command=lambda: self.filtrar_tarefas('todas'), width=18).grid(row=len(botoes)+2, column=0, pady=2, sticky="ew")
        ttk.Button(parent, text="⏳ Pendentes", command=lambda: self.filtrar_tarefas('pendentes'), width=18).grid(row=len(botoes)+3, column=0, pady=2, sticky="ew")
        ttk.Button(parent, text="✅ Concluídas", command=lambda: self.filtrar_tarefas('concluidas'), width=18).grid(row=len(botoes)+4, column=0, pady=2, sticky="ew")
    
    def criar_treeview(self, parent):
        """Cria a tabela de tarefas"""
        # Frame para treeview e scrollbar
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=0, column=0, sticky="nsew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Treeview
        columns = ('Status', 'Descrição', 'Prioridade', 'Data Término')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', 
                                style='Custom.Treeview', height=15)
        
        # Configurar colunas
        self.tree.heading('Status', text='Status')
        self.tree.heading('Descrição', text='Descrição')
        self.tree.heading('Prioridade', text='Prioridade')
        self.tree.heading('Data Término', text='Data Término')
        
        self.tree.column('Status', width=80, anchor='center')
        self.tree.column('Descrição', width=300, anchor='w')
        self.tree.column('Prioridade', width=100, anchor='center')
        self.tree.column('Data Término', width=120, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind duplo clique para editar
        self.tree.bind('<Double-1>', lambda e: self.editar_tarefa())
    
    def criar_estatisticas(self, parent):
        """Cria painel de estatísticas"""
        self.label_stats = ttk.Label(parent, text="", font=('Segoe UI', 10))
        self.label_stats.grid(row=0, column=0, sticky="w")
    
    def carregar_tarefas(self):
        """Carrega tarefas do arquivo JSON"""
        try:
            if os.path.exists(self.nome_arquivo):
                with open(self.nome_arquivo, 'r', encoding='utf-8') as file:
                    return json.load(file)
            return []
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def salvar_tarefas(self):
        """Salva tarefas no arquivo JSON"""
        try:
            with open(self.nome_arquivo, 'w', encoding='utf-8') as file:
                json.dump(self.tarefas, file, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar tarefas: {str(e)}")
    
    def atualizar_lista(self, filtro='todas'):
        """Atualiza a lista de tarefas"""
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Aplicar filtro
        tarefas_filtradas = self.aplicar_filtro(filtro)
        
        # Adicionar tarefas
        for i, tarefa in enumerate(tarefas_filtradas):
            status = "✅" if tarefa.get('concluida', False) else "⏳"
            descricao = tarefa.get('descricao', '')
            prioridade = self.formatar_prioridade(tarefa.get('prioridade', 'Sem prioridade'))
            data_termino = tarefa.get('data_termino', 'Sem data')
            
            # Tags para coloração
            tags = []
            if tarefa.get('concluida', False):
                tags.append('concluida')
            elif self.tarefa_atrasada(tarefa):
                tags.append('atrasada')
            elif tarefa.get('prioridade') == 'Alta':
                tags.append('alta_prioridade')
            
            self.tree.insert('', 'end', values=(status, descricao, prioridade, data_termino), tags=tags)
        
        # Configurar tags de cor
        self.tree.tag_configure('concluida', foreground='#28a745')
        self.tree.tag_configure('atrasada', foreground='#dc3545', background='#f8d7da')
        self.tree.tag_configure('alta_prioridade', foreground='#dc3545')
        
        # Atualizar estatísticas
        self.atualizar_estatisticas()
    
    def aplicar_filtro(self, filtro):
        """Aplica filtro às tarefas"""
        if filtro == 'pendentes':
            return [t for t in self.tarefas if not t.get('concluida', False)]
        elif filtro == 'concluidas':
            return [t for t in self.tarefas if t.get('concluida', False)]
        else:
            return self.tarefas
    
    def formatar_prioridade(self, prioridade):
        """Adiciona ícones às prioridades"""
        if prioridade == 'Alta':
            return "🔴 Alta"
        elif prioridade == 'Média':
            return "🟡 Média"
        elif prioridade == 'Baixa':
            return "🟢 Baixa"
        return prioridade
    
    def tarefa_atrasada(self, tarefa):
        """Verifica se tarefa está atrasada"""
        if tarefa.get('concluida', False):
            return False
        
        data_str = tarefa.get('data_termino')
        if data_str and data_str != 'Sem data':
            try:
                data_termino = datetime.strptime(data_str, "%d/%m/%Y")
                return datetime.now() > data_termino
            except ValueError:
                pass
        return False
    
    def atualizar_estatisticas(self):
        """Atualiza painel de estatísticas"""
        total = len(self.tarefas)
        concluidas = sum(1 for t in self.tarefas if t.get('concluida', False))
        pendentes = total - concluidas
        atrasadas = sum(1 for t in self.tarefas if self.tarefa_atrasada(t))
        
        progresso = (concluidas / total * 100) if total > 0 else 0
        
        texto_stats = f"📊 Total: {total} | ✅ Concluídas: {concluidas} | ⏳ Pendentes: {pendentes} | ⚠️ Atrasadas: {atrasadas} | 📈 Progresso: {progresso:.1f}%"
        self.label_stats.config(text=texto_stats)
    
    def adicionar_tarefa(self):
        """Abre diálogo para adicionar nova tarefa"""
        dialog = TaskDialog(self.root, "Adicionar Nova Tarefa")
        if dialog.resultado:
            nova_tarefa = {
                'descricao': dialog.resultado['descricao'],
                'prioridade': dialog.resultado['prioridade'],
                'data_termino': dialog.resultado['data_termino'],
                'concluida': False
            }
            self.tarefas.append(nova_tarefa)
            self.salvar_tarefas()
            self.atualizar_lista()
            messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
    
    def editar_tarefa(self):
        """Edita tarefa selecionada"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para editar!")
            return
        
        # Obter índice da tarefa na lista original
        item_index = self.tree.index(selection[0])
        
        # Encontrar a tarefa correspondente (considerando filtros)
        tarefas_visiveis = self.aplicar_filtro('todas')  # ou o filtro atual
        if item_index < len(tarefas_visiveis):
            tarefa_atual = tarefas_visiveis[item_index]
            tarefa_index = self.tarefas.index(tarefa_atual)
            
            dialog = TaskDialog(self.root, "Editar Tarefa", tarefa_atual)
            if dialog.resultado:
                self.tarefas[tarefa_index].update(dialog.resultado)
                self.salvar_tarefas()
                self.atualizar_lista()
                messagebox.showinfo("Sucesso", "Tarefa atualizada com sucesso!")
    
    def marcar_concluida(self):
        """Marca/desmarca tarefa como concluída"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma tarefa!")
            return
        
        item_index = self.tree.index(selection[0])
        tarefas_visiveis = self.aplicar_filtro('todas')
        
        if item_index < len(tarefas_visiveis):
            tarefa_atual = tarefas_visiveis[item_index]
            tarefa_index = self.tarefas.index(tarefa_atual)
            
            # Alternar status
            status_atual = self.tarefas[tarefa_index].get('concluida', False)
            self.tarefas[tarefa_index]['concluida'] = not status_atual
            
            self.salvar_tarefas()
            self.atualizar_lista()
            
            status_texto = "concluída" if not status_atual else "pendente"
            messagebox.showinfo("Sucesso", f"Tarefa marcada como {status_texto}!")
    
    def remover_tarefa(self):
        """Remove tarefa selecionada"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para remover!")
            return
        
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja remover esta tarefa?"):
            item_index = self.tree.index(selection[0])
            tarefas_visiveis = self.aplicar_filtro('todas')
            
            if item_index < len(tarefas_visiveis):
                tarefa_atual = tarefas_visiveis[item_index]
                self.tarefas.remove(tarefa_atual)
                
                self.salvar_tarefas()
                self.atualizar_lista()
                messagebox.showinfo("Sucesso", "Tarefa removida com sucesso!")
    
    def filtrar_tarefas(self, filtro):
        """Aplica filtro e atualiza lista"""
        self.atualizar_lista(filtro)


class TaskDialog:
    """Diálogo para adicionar/editar tarefas"""
    def __init__(self, parent, titulo, tarefa_existente=None):
        self.resultado = None
        
        # Criar janela
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(titulo)
        self.dialog.geometry("400x300")
        self.dialog.configure(bg='#f8f9fa')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centralizar
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (400 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (300 // 2)
        self.dialog.geometry(f"400x300+{x}+{y}")
        
        self.criar_campos(tarefa_existente)
        
        # Esperar resultado
        self.dialog.wait_window()
    
    def criar_campos(self, tarefa_existente):
        """Cria campos do formulário"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Descrição
        ttk.Label(main_frame, text="Descrição:", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        self.entry_descricao = ttk.Entry(main_frame, width=50, font=('Segoe UI', 10))
        self.entry_descricao.pack(fill='x', pady=(5, 15))
        
        # Prioridade
        ttk.Label(main_frame, text="Prioridade:", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        self.combo_prioridade = ttk.Combobox(main_frame, values=['Baixa', 'Média', 'Alta'], 
                                           state='readonly', font=('Segoe UI', 10))
        self.combo_prioridade.pack(fill='x', pady=(5, 15))
        
        # Data
        ttk.Label(main_frame, text="Data de Término (DD/MM/AAAA):", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        self.entry_data = ttk.Entry(main_frame, width=50, font=('Segoe UI', 10))
        self.entry_data.pack(fill='x', pady=(5, 15))
        
        # Preencher campos se editando
        if tarefa_existente:
            self.entry_descricao.insert(0, tarefa_existente.get('descricao', ''))
            if tarefa_existente.get('prioridade') in ['Baixa', 'Média', 'Alta']:
                self.combo_prioridade.set(tarefa_existente.get('prioridade'))
            data = tarefa_existente.get('data_termino', '')
            if data and data != 'Sem data':
                self.entry_data.insert(0, data)
        
        # Botões
        frame_botoes = ttk.Frame(main_frame)
        frame_botoes.pack(fill='x', pady=(20, 0))
        
        ttk.Button(frame_botoes, text="Salvar", command=self.salvar).pack(side='right', padx=(10, 0))
        ttk.Button(frame_botoes, text="Cancelar", command=self.dialog.destroy).pack(side='right')
        
        # Focus no primeiro campo
        self.entry_descricao.focus_set()
    
    def salvar(self):
        """Salva os dados do formulário"""
        descricao = self.entry_descricao.get().strip()
        if not descricao:
            messagebox.showwarning("Aviso", "Digite uma descrição para a tarefa!")
            return
        
        prioridade = self.combo_prioridade.get() or 'Sem prioridade'
        data = self.entry_data.get().strip()
        
        # Validar data se fornecida
        if data:
            try:
                datetime.strptime(data, "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA")
                return
        else:
            data = 'Sem data'
        
        self.resultado = {
            'descricao': descricao,
            'prioridade': prioridade,
            'data_termino': data
        }
        
        self.dialog.destroy()


def main():
    """Função principal"""
    root = tk.Tk()
    app = GerenciadorTarefasGUI(root)
    
    # Protocolo de fechamento
    def on_closing():
        app.salvar_tarefas()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()