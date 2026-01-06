import datetime
import os

class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.users = {}
        self.file = None
        self._ensure_file()
        self.load()

    def _ensure_file(self):
        # Cria o arquivo se não existir
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                pass

    def load(self):
        self.file = open(self.filename, "r", encoding="utf-8")
        self.users = {}
        for line in self.file:
            line = line.strip()
            if not line:
                continue  # ignora linhas vazias
            parts = line.split(";")
            if len(parts) != 4:
                # opcional: logar a linha malformada
                # print(f"Linha inválida no arquivo: {line}")
                continue
            email, password, name, created = parts
            self.users[email] = (password, name, created)
        self.file.close()

    def get_user(self, email):
        if email in self.users:
            return self.users[email]
        else:
            return -1

    def add_user(self, email, password, name):
        email = str(email).strip()
        #chamar função para mudar a senha
        password = str(password).strip()
        name = str(name).strip()

        if email in self.users:
            print("E-mail já existente!")
            return -1

        self.users[email] = (password, name, DataBase.get_date())
        self.save()
        return 1

    def validate(self, email, password):
        user = self.get_user(email)
        if user == -1:
            return False
        return user[0] == password

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            for email, (password, name, created) in self.users.items():
                f.write(f"{email};{password};{name};{created}\n")

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]
