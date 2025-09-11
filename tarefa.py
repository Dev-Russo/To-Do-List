# tarefa.py - Nova classe para representar uma tarefa
"""
Classe Tarefa - Representa uma tarefa individual com seus atributos e métodos
"""
from datetime import datetime
from constantes import FORMATO_DATA

class Tarefa:
    def __init__(self, descricao, prioridade=None, data_termino=None):
        """
        Inicializa uma nova tarefa
        
        Args:
            descricao (str): Descrição da tarefa
            prioridade (str): Prioridade da tarefa (Baixa, Média, Alta)
            data_termino (str ou datetime): Data limite para conclusão
        """
        self.descricao = descricao
        self.concluida = False
        self.prioridade = prioridade or "Sem prioridade"
        
        # Converte data_termino para string se for datetime
        if isinstance(data_termino, datetime):
            self.data_termino = data_termino.strftime(FORMATO_DATA)
        else:
            self.data_termino = data_termino or "Sem data de término"
    
    def marcar_concluida(self):
        """Marca a tarefa como concluída"""
        self.concluida = True
    
    def marcar_pendente(self):
        """Marca a tarefa como pendente"""
        self.concluida = False
    
    def alterar_descricao(self, nova_descricao):
        """Altera a descrição da tarefa"""
        self.descricao = nova_descricao
    
    def alterar_prioridade(self, nova_prioridade):
        """Altera a prioridade da tarefa"""
        self.prioridade = nova_prioridade
    
    def alterar_data_termino(self, nova_data):
        """Altera a data de término da tarefa"""
        if isinstance(nova_data, datetime):
            self.data_termino = nova_data.strftime(FORMATO_DATA)
        else:
            self.data_termino = nova_data
    
    def get_status(self):
        """Retorna o status da tarefa como string"""
        return "Concluída" if self.concluida else "Pendente"
    
    def get_data_datetime(self):
        """Converte data_termino de string para datetime, se possível"""
        try:
            if self.data_termino and self.data_termino != "Sem data de término":
                return datetime.strptime(self.data_termino, FORMATO_DATA)
        except ValueError:
            pass
        return None
    
    def esta_atrasada(self):
        """Verifica se a tarefa está atrasada (passou da data e não foi concluída)"""
        if self.concluida:
            return False
        
        data_limite = self.get_data_datetime()
        if data_limite:
            return datetime.now() > data_limite
        return False
    
    def to_dict(self):
        """Converte a tarefa para dicionário (para salvar em JSON)"""
        return {
            'descricao': self.descricao,
            'concluida': self.concluida,
            'prioridade': self.prioridade,
            'data_termino': self.data_termino
        }
    
    @classmethod
    def from_dict(cls, dados):
        """Cria uma tarefa a partir de um dicionário (carregando do JSON)"""
        tarefa = cls(
            descricao=dados['descricao'],
            prioridade=dados.get('prioridade'),
            data_termino=dados.get('data_termino')
        )
        tarefa.concluida = dados.get('concluida', False)
        return tarefa
    
    def __str__(self):
        """Representação em string da tarefa"""
        return f"{self.descricao} - {self.prioridade} - {self.get_status()} - {self.data_termino}"
    
    def __repr__(self):
        """Representação técnica da tarefa"""
        return f"Tarefa('{self.descricao}', '{self.prioridade}', '{self.data_termino}', {self.concluida})"


