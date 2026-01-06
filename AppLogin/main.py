from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase

#para mudar a cor do fundo da tela
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

#Mudar senha para base 64
import base64

#size largura, altura

#cada classe para sua tela
class CreateAccountWindow(Screen):
    name_field = ObjectProperty(None)   # não use "name" porque conflita com Screen.name
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    
    #para mudar a cor do fundo da tela
    Window.clearcolor = get_color_from_hex("#297EEE")

    def submit(self):
        if self.email.text != "":
            if self.name_field.text != "":
                if self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
                    if self.password.text != "":
                        senha_criptp = criptrografar_senha(self.password.text, self.email.text)
                        result = db.add_user(self.email.text, senha_criptp, self.name_field.text)
                        if result == 1:
                            self.reset()
                            sm.current = "login"
                        else:
                            invalidForm(1)  # ou popup específico "Email já existe"
                    else:
                        invalidForm(2) # senha não iformada
                else:
                    invalidForm(3) #email inválido
            else:
                invalidForm(4) #Nome não informado
        else:
            invalidForm(5) #email não informado


    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.name_field.text = ""

#cada classe para sua tela
class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        senha_criptp = criptrografar_senha(self.password.text, self.email.text)
        if db.validate(self.email.text, senha_criptp):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""

#cada classe para sua tela
class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        user = db.get_user(self.current)
        if user == -1:
            invalidLogin()
            sm.current = "login"
            return

        password, name, created = user
        self.n.text = "Nome: " + name
        self.email.text = "E-mail: " + self.current
        self.created.text = "Criado em: " + created

#Classe obrigatório para o funcionamento do sistema, porém não é utilizada nesse caso
class WindowManager(ScreenManager):
    pass

def invalidLogin():
    pop = Popup(title='Login Inválido', content=Label(text='Nome ou senha inválido!.'), size_hint=(None, None), size=(265, 150))
    pop.open()

#possíveis erros ao fazer login
def invalidForm(cod_erro):
    if cod_erro == 1:
        msg = "E-mail já existe"
    elif cod_erro == 2:
        msg = "Senha não informada"
    elif cod_erro == 3:
        msg = "E-mail inválido, sem (.) ou sem (@)"
    elif cod_erro == 4:
        msg = "Nome não informado"
    else:
        msg = "E-mail não informado" 
    pop = Popup(title='Atenção', content=Label(text=msg), size_hint=(None, None), size=(265, 150))
    pop.open()

#instanciando as clases
kv = Builder.load_file("mK.kv")
sm = WindowManager()
db = DataBase("users.txt")
#rodrigo@rodrigo.com.br;MTIzNEA=;Rodrigo;2026-01-06
def criptrografar_senha(password, email):
    senha_bytes_senha = password.encode('ascii')
    senha_bytes_email = email.encode('ascii')
    senha_bytes_final = senha_bytes_senha + senha_bytes_email
    base64_bytes = base64.b64encode(senha_bytes_final)
    senha_ascii_final = base64_bytes.decode('ascii')
    return senha_ascii_final

#criando as telas
screens = [
    LoginWindow(name="login"),
    CreateAccountWindow(name="create"),
    MainWindow(name="main")
]

#adicionando as telas no widget
for screen in screens:
    sm.add_widget(screen)
sm.current = "login"

class MyMainApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    MyMainApp().run()
