import mysql.connector
import heapq

db_config = {
    'user': 'turma6ntop',
    'password': 'turma6ntop',
    'host': 'db4free.net',
    'database': 'linkedin6n',
    'port': 3306
}

class Usuario:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

    def salvar_no_banco(self):
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO usuarios (nome, email) VALUES (%s, %s)', (self.nome, self.email))
            conn.commit()
            print("Usuário cadastrado com sucesso!")
        except mysql.connector.Error as erro:
            conn.rollback()
            print(f"Ocorreu um erro ao cadastrar o usuário: {erro}")
        finally:
            conn.close()

    @staticmethod
    def listar_usuarios():
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM usuarios')
        usuarios = cursor.fetchall()

        conn.close()
        return usuarios

    @staticmethod
    def excluir_do_banco(id):
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        try:
            cursor.execute('DELETE FROM usuarios WHERE id = %s', (id,))
            conn.commit()
            print("Usuário excluído com sucesso!")
        except mysql.connector.Error as erro:
            conn.rollback()
            print(f"Ocorreu um erro ao excluir o usuário: {erro}")
        finally:
            conn.close()

class Contato:
    def __init__(self, nome, perfil_linkedin):
        self.nome = nome
        self.perfil_linkedin = perfil_linkedin

    def salvar_no_banco(self):
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM contatos WHERE perfil_linkedin = %s', (self.perfil_linkedin,))
            if cursor.fetchone() is None:
                cursor.execute('INSERT INTO contatos (nome, perfil_linkedin) VALUES (%s, %s)', (self.nome, self.perfil_linkedin))
                conn.commit()
                print("Contato cadastrado com sucesso!")
            else:
                print("Contato já cadastrado.")
        except mysql.connector.Error as erro:
            print(f"Ocorreu um erro {erro}. Tente novamente.")
        finally:
            conn.close()

    @staticmethod
    def listar_contatos():
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM contatos')
        contatos = cursor.fetchall()

        conn.close()
        return contatos

    @staticmethod
    def excluir_contato(id):
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM conexoes WHERE contato1_id = %s OR contato2_id = %s', (id, id))
        cursor.execute('DELETE FROM contatos WHERE id = %s', (id,))

        conn.commit()
        conn.close()

class Conexao:
    @staticmethod
    def adicionar_conexao(contato1_id, contato2_id):
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('BEGIN')
        
        try:
            cursor.execute('SELECT * FROM conexoes WHERE (contato1_id = %s AND contato2_id = %s) OR (contato1_id = %s AND contato2_id = %s)',
                          (contato1_id, contato2_id, contato2_id, contato1_id))

            if cursor.fetchone() is None:
                cursor.execute('INSERT INTO conexoes (contato1_id, contato2_id) VALUES (%s, %s)', (contato1_id, contato2_id))
            else:
                print("A conexão entre esses contatos já existe.")
            
            conn.commit()
            
        except mysql.connector.Error as erro:
            conn.rollback()
            print(f"Ocorreu um erro {erro}. Tente novamente.")
            
        conn.close()

    @staticmethod
    def listar_conexoes(contato_id):
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT contatos.id, contatos.nome
            FROM contatos
            JOIN conexoes ON contatos.id = CASE
                WHEN conexoes.contato1_id = %s THEN conexoes.contato2_id
                ELSE conexoes.contato1_id
            END
            WHERE conexoes.contato1_id = %s OR conexoes.contato2_id = %s
        ''', (contato_id, contato_id, contato_id))

        conexoes = cursor.fetchall()
        conn.close()
        return conexoes

    @staticmethod
    def excluir_conexao(id1, id2):
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM conexoes WHERE (contato1_id = %s AND contato2_id = %s) OR (contato1_id = %s AND contato2_id = %s)', (id1, id2, id2, id1))

        conn.commit()
        conn.close()

def menu():
    while True:
        print("\n1. Cadastrar Usuário")
        print("2. Listar Usuários")
        print("3. Excluir Usuário")
        print("4. Cadastrar Contato")
        print("5. Listar Contatos")
        print("6. Excluir Contato")
        print("7. Adicionar Conexão")
        print("8. Listar Conexões de um Contato")
        print("9. Excluir Conexão")
        print("0. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            nome = input("Digite o nome do usuário: ")
            email = input("Digite o e-mail do usuário: ")
            usuario = Usuario(nome, email)
            usuario.salvar_no_banco()
        elif escolha == "2":
            usuarios = Usuario.listar_usuarios()
            print("Lista de Usuários:")
            for usuario in usuarios:
                print(f"ID: {usuario[0]}, Nome: {usuario[1]}, E-mail: {usuario[2]}")
        elif escolha == "3":
            id_usuario = int(input("Digite o ID do usuário que deseja excluir: "))
            Usuario.excluir_do_banco(id_usuario)
        elif escolha == "4":
            nome = input("Nome do contato: ")
            perfil_linkedin = input("Perfil do LinkedIn: ")
            contato = Contato(nome, perfil_linkedin)
            contato.salvar_no_banco()
        elif escolha == "5":
            contatos = Contato.listar_contatos()
            print("Lista de Contatos:")
            for contato in contatos:
                print(f"ID: {contato[0]}, Nome: {contato[1]}, Perfil LinkedIn: {contato[2]}")
        elif escolha == "6":
            id_contato = int(input("Digite o ID do contato que deseja excluir: "))
            Contato.excluir_contato(id_contato)
        elif escolha == "7":
            contato1_id = int(input("ID do primeiro contato: "))
            contato2_id = int(input("ID do segundo contato: "))
            Conexao.adicionar_conexao(contato1_id, contato2_id)
        elif escolha == "8":
            contato_id = int(input("ID do contato: "))
            conexoes = Conexao.listar_conexoes(contato_id)
            print("Conexões do Contato:")
            for conexao in conexoes:
                print(f"ID: {conexao[0]}, Nome: {conexao[1]}")
        elif escolha == "9":
            id1 = int(input("Informe o ID do primeiro contato: "))
            id2 = int(input("Informe o ID do segundo contato: "))
            Conexao.excluir_conexao(id1, id2)
        elif escolha == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
