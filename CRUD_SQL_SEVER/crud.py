import pyodbc
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
#cores em hex
from kivy.utils import get_color_from_hex
#Layout para o grid fr clientes
from kivy.graphics import Color, Rectangle

# --- Conexão com SQL Server ---
def get_connection():
    # Ajuste os parâmetros conforme seu ambiente
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=Server\SQLEXPRESS;'
        'DATABASE=clientes;'
        'UID=sa;'
        'PWD=1234;'
    )
    return conn

#cria a tabela caso não exista
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Clientes' AND xtype='U')
        CREATE TABLE Clientes (
            id INT IDENTITY(1,1) PRIMARY KEY,
            nome NVARCHAR(100),
            sobrenome NVARCHAR(100),
            email NVARCHAR(100),
            cpf NVARCHAR(20)
        )
    """)
    conn.commit()
    conn.close()

class ClienteApp(App):
    def build(self):
        init_db()

        # Layout raiz
        self.root_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Plano de fundo como imagem no canvas.before
        with self.root_layout.canvas.before:
            self.bg_rect = Rectangle(
                source="C:/Users/Rodrigo Santos/Documents/Bradesco/Python/Projeto/SQL_Lite/ProjetoSQL/FundoSistema.jpg",
                pos=self.root_layout.pos,
                size=self.root_layout.size
            )
        # Atualiza quando o layout muda
        self.root_layout.bind(pos=self.update_bg, size=self.update_bg)

        # Campos
        form_layout = GridLayout(cols=2, spacing=5, size_hint=(1, None), height=200)

        form_layout.add_widget(Label(text="Nome:", bold=True, color=get_color_from_hex("#F7DF04"), font_size=20))
        self.nome_input = TextInput()
        form_layout.add_widget(self.nome_input)

        form_layout.add_widget(Label(text="Sobrenome:", bold=True, color=get_color_from_hex("#F7DF04"), font_size=20))  # vermelho
        self.sobrenome_input = TextInput()
        form_layout.add_widget(self.sobrenome_input)

        form_layout.add_widget(Label(text="Email:", bold=True, color=get_color_from_hex("#F7DF04"), font_size=20))
        self.email_input = TextInput()
        form_layout.add_widget(self.email_input)

        form_layout.add_widget(Label(text="CPF:", bold=True, color=get_color_from_hex("#F7DF04"), font_size=20))
        self.cpf_input = TextInput()
        form_layout.add_widget(self.cpf_input)

        self.root_layout.add_widget(form_layout)

        # Botões
        btn_layout = GridLayout(cols=4, spacing=5, size_hint=(1, None), height=50)
        btn_layout.add_widget(Button(text="Criar", color=get_color_from_hex("#F7DF04"), bold=True, background_color=get_color_from_hex("#F5091DFF"), font_size=20, on_press=self.criar_cliente))
        btn_layout.add_widget(Button(text="Atualizar", color=get_color_from_hex("#F7DF04"), bold=True, background_color=get_color_from_hex("#F5091DFF"), font_size=20, on_press=self.atualizar_cliente))
        btn_layout.add_widget(Button(text="Deletar", color=get_color_from_hex("#F7DF04"), bold=True, background_color=get_color_from_hex("#F5091DFF"), font_size=20, on_press=self.deletar_cliente))
        btn_layout.add_widget(Button(text="Visualizar Todos", color=get_color_from_hex("#F7DF04"), bold=True, background_color=get_color_from_hex("#F5091DFF"), font_size=20, on_press=self.visualizar_clientes))
        self.root_layout.add_widget(btn_layout)

        self.result_area = ScrollView(size_hint=(1, 1))
        self.result_label = Label(size_hint_y=None, text="", valign="top", )
        # Faz o label crescer com o texto e quebrar linha corretamente
        self.result_label.bind(texture_size=self._update_result_label_size)
        self.result_area.add_widget(self.result_label)
        self.root_layout.add_widget(self.result_area)
        return self.root_layout
    
    # Atualiza posição/tamanho do plano de fundo
    def update_bg(self, *args):
        self.bg_rect.pos = self.root_layout.pos
        self.bg_rect.size = self.root_layout.size

    # Ajusta o label dentro do ScrollView para acompanhar o texto
    def _update_result_label_size(self, instance, value):
        # Define a altura baseada na textura e faz o texto ocupar a largura do ScrollView
        self.result_label.height = value[1]
        self.result_label.text_size = (self.result_area.width, None)    

    # --- Funções CRUD ---
    def criar_cliente(self, instance):
        conn = get_connection()
        cursor = conn.cursor()
        erro = 0
        if self.nome_input.text == "" or self.sobrenome_input == "" or self.email_input == "" or self.cpf_input == "":
            invalidForm(1)
            erro = 1
        
        if self.cpf_input != "":
            cursor.execute("SELECT COUNT(*) FROM Clientes WHERE cpf=?", (self.cpf_input.text,))
            existe = cursor.fetchone()[0]
        
        # Inserir novo cliente
        if existe == 0 and erro == 0:
            cursor.execute("INSERT INTO Clientes (nome, sobrenome, email, cpf) VALUES (?, ?, ?, ?)",
                           (self.nome_input.text, self.sobrenome_input.text, self.email_input.text, self.cpf_input.text))
            conn.commit()
            Save_OK(1)
            self.limpar_campos()

        conn.close() 
                               

    def atualizar_cliente(self, instance):
        conn = get_connection()
        cursor = conn.cursor()        
        cursor.execute("SELECT COUNT(*) FROM Clientes WHERE cpf=?", (self.cpf_input.text,))
        existe = cursor.fetchone()[0]
        print("existe", existe)
        if self.cpf_input.text != "" and existe > 0:
            #Criar layout do popup
            box = BoxLayout(orientation="vertical", spacing=10, padding=10)
            box.add_widget(Label(text=f"Tem certeza que deseja atualizar o cliente com CPF {self.cpf_input.text}?"))

            btns = BoxLayout(spacing=10, size_hint=(1, None), height=40)
            btn_confirmar = Button(text="Confirmar")
            btn_cancelar = Button(text="Cancelar")
            btns.add_widget(btn_confirmar)
            btns.add_widget(btn_cancelar)
            box.add_widget(btns)

            popup = Popup(title="Confirmação de Atualização",
                        content=box,
                        size_hint=(None, None), size=(470, 200),
                        auto_dismiss=False)               

            # Função para confirmar atualização
            def confirmar_atualizacao(instance):
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE Clientes SET nome=?, sobrenome=?, email=? WHERE cpf=?",
                                (self.nome_input.text, self.sobrenome_input.text, self.email_input.text, self.cpf_input.text))
                conn.commit()
                conn.close()
                Save_OK(2)
                self.limpar_campos()
                popup.dismiss()

            # Função para cancelar
            def cancelar_atualizacao(instance):
                invalidForm(2)
                popup.dismiss()

            btn_confirmar.bind(on_press=confirmar_atualizacao)
            btn_cancelar.bind(on_press=cancelar_atualizacao)

            popup.open()            
        elif self.cpf_input.text != "" and existe == 0:
            invalidForm(4)
        elif self.cpf_input.text == "":
            invalidForm(5)
       
    def deletar_cliente(self, instance):
        conn = get_connection()
        cursor = conn.cursor()        
        cursor.execute("SELECT COUNT(*) FROM Clientes WHERE cpf=?", (self.cpf_input.text,))
        existe = cursor.fetchone()[0]
        print("existe", existe)
        if self.cpf_input.text != "" and existe > 0:                    
            # Criar layout do popup
            box = BoxLayout(orientation="vertical", spacing=10, padding=10)
            box.add_widget(Label(text=f"Tem certeza que deseja excluir o cliente com CPF {self.cpf_input.text}?"))

            btns = BoxLayout(spacing=10, size_hint=(1, None), height=40)
            btn_confirmar = Button(text="Confirmar")
            btn_cancelar = Button(text="Cancelar")
            btns.add_widget(btn_confirmar)
            btns.add_widget(btn_cancelar)
            box.add_widget(btns)

            popup = Popup(title="Confirmação de Exclusão",
                        content=box,
                        size_hint=(None, None), size=(420, 200),
                        auto_dismiss=False)

            # Função para confirmar exclusão
            def confirmar_exclusao(instance):
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Clientes WHERE cpf=?", (self.cpf_input.text,))
                conn.commit()
                conn.close()
                Save_OK(3)
                self.limpar_campos()
                popup.dismiss()

            # Função para cancelar
            def cancelar_exclusao(instance):
                invalidForm(3)
                popup.dismiss()

            btn_confirmar.bind(on_press=confirmar_exclusao)
            btn_cancelar.bind(on_press=cancelar_exclusao)

            popup.open()
        
        elif self.cpf_input.text != "" and existe == 0:
            invalidForm(6)
        elif self.cpf_input.text == "":
            invalidForm(7)         
    
    def visualizar_clientes(self, instance):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, sobrenome, email, cpf FROM Clientes")
        rows = cursor.fetchall()
        conn.close()

        # Limpa a área antes de adicionar nova grid
        self.result_area.clear_widgets()

        # Cria grid com 5 colunas (ID, Nome, Sobrenome, Email, CPF)
        grid = GridLayout(cols=5, spacing=20, padding=[0, 10, 0, 10], size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        # === Fundo branco ===
        with grid.canvas.before:
            Color(1, 1, 1, 1)  # branco RGBA
            self.rect = Rectangle(size=grid.size, pos=grid.pos)

        # Atualiza retângulo quando o grid mudar de tamanho/posição
        def update_rect(instance, value):
            self.rect.pos = instance.pos
            self.rect.size = instance.size

        grid.bind(pos=update_rect, size=update_rect)

        # Cabeçalho
        headers = ["ID", "Nome", "Sobrenome", "Email", "CPF"]
        for h in headers:
            grid.add_widget(Label(
                text=h,
                bold=True,
                font_size=18,
                #color=(1, 1, 0, 1)  # amarelo
                color=get_color_from_hex("#06048D")
            ))

        # Linhas da tabela
        for row in rows:
            for cell in row:
                grid.add_widget(Label(
                    text=str(cell),
                    font_size=16,
                    color=(0, 0, 0, 1)  # preto para contraste no fundo branco
                ))

        # Adiciona grid dentro do ScrollView
        self.result_area.add_widget(grid)
        

    def limpar_campos(self):
        self.nome_input.text = ""
        self.sobrenome_input.text = ""
        self.email_input.text = ""
        self.cpf_input.text = ""             
        
def invalidForm(cod_erro):
    if cod_erro == 1:
        msg = "Favor preencher os campos obrigatórios: Nome, Sobrenome, Email e CPF!"
        largura = 530
        altura = 150
    elif cod_erro == 2:
        msg = "Atualização cancelada."
        largura = 265
        altura = 150        
    elif cod_erro == 2:
        msg = "Exclusão cancelada."
        largura = 265
        altura = 150        
    elif cod_erro == 4:
        msg = "CPF inexistente para atualização!"
        largura = 265
        altura = 150         
    elif cod_erro == 5:
        msg = "CPF não informado para atualização!" 
        largura = 265
        altura = 150
    elif cod_erro == 6:
        msg = "CPF inexistente para exclusão!" 
        largura = 265
        altura = 150 
    elif cod_erro == 7:
        msg = "CPF não informado para exclusão!" 
        largura = 265
        altura = 150                                 

    #pop = Popup(title='Atenção', content=Label(text=msg), size_hint=(None, None), size=(265, 150))
    pop = Popup(title='Atenção', content=Label(text=msg), size_hint=(None, None), size=(largura, altura))
    pop.open()
    
def Save_OK(cod_erro):
    if cod_erro == 1:
        msg = "Cliente criado com sucesso!"
    elif cod_erro == 2:
        msg = "Cliente atualizado com sucesso!"
    else:
        msg = "liente deletado com sucesso!"
    pop = Popup(title='Atenção', content=Label(text=msg), size_hint=(None, None), size=(265, 150))
    pop.open()            

if __name__ == "__main__":
    ClienteApp().run()
