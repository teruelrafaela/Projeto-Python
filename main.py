import re
import os
import smtplib
import openpyxl
import email
from email.message import EmailMessage
from time import sleep
import pandas as pd
import pywhatkit as kit

class toDo:

    def iniciar(self):
    #     self.lista_tarefas = []
    #     self.email_destino()
    #     self.menu()
    #     self.criar_planilha()
    #     sleep (1)
    #     self.enviar_email()
        self.enviar_whats()

    def email_destino (self):
        while True:
            self.email = str(input('Email de destino:')).lower()
            padrao_email = re.search(
            '^[a-z0-9._]+@[a-z0-9]+.[a-z]+(.[a-z])?$', self.email
            )
            if padrao_email:
                print('Email válido')
                break
            else:
                print ('Email inválido, tente outro')

    def menu (self):
        while True:
            menu_principal = int(input("""
            MENU PRINCIPAL
            [1] CADASTRAR
            [2] VISUALIZAR                          
            [3] SAIR
            Opção: """))

            match menu_principal:
                case 1: self.cadastrar()
                case 2: self.visualizar()
                case 3:break
                case _:print('\nOpção Inválida')
                 
    def cadastrar(self):
        while True:
            self.tarefa = str(input('Digite uma tarefa ou [S] para sair:')).capitalize()
            if self.tarefa == 'S':
                break
            else:
                self.lista_tarefas.append(self.tarefa)
                try:
                    with open ('./src/Tarefas/historico_tarefas.txt', 'a', encoding='utf8') as arquivo:
                        arquivo.write(f'{self.tarefa}\n')
                except FileNotFoundError as e:
                    print(f'nError:{e}') 

    def visualizar(self):
        try:
            with open ('./src/Tarefas/historico_tarefas.txt', 'r', encoding='utf=8') as arquivo:
                print(arquivo.read())
        except FileExistsError as e:
                print(f'Erro:{e}')

    def criar_planilha(self):
        if len(self.lista_tarefas)> 0:
            try:
                df = pd.DataFrame({"Tarefas": self.lista_tarefas})
                self.nome_arquivo =str(input('Nome do arquivo: ')).lower()

                if self.nome_arquivo[-5:] == '.xlsx':
                    df.to_excel(f'./src/Tarefas/{self.nome_arquivo}', index = False)
                else:
                    df.to_excel (f'./src/Tarefas/{self.nome_arquivo}.xlsx', index= False)

                print('n\Planilha criada com sucesso!')

            except Exception as e:
                    print (f'erro: {e}')
        else:
            print('\nLista de tarefas vazia')    

    def enviar_email(self):
        endereco = '...@gmail.com'
        with open ('./src/Senha/Senha.txt','r',encoding='utf8') as arquivo:
            s= arquivo.readlines()
        senha=s[0]

        msg = EmailMessage ()
        msg ['From'] = endereco
        msg['To']= self.email
        msg['Subject'] = 'Oooo zé, chegou a planilha!'

        msg.set_content(
              'Planilha em anexo'
         )
        arquivos = [f'./src/Tarefas/{self.nome_arquivo}.xlsx']

        for arquivo in arquivos:
            with open(arquivo, 'rb') as arq:
                   dados = arq.read()
                   nome_arquivo = arq.name
            msg.add_attachment(
                     dados,
                     maintype='application',
                     subtype='octet-stream',
                     filename=nome_arquivo

                )
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(endereco,senha, initial_response_ok=True)
        server.send_message(msg)
        print('Email enviado com sucesso')

    def enviar_whats(self):
        try:
            numero_destino = '+5511'
            mensagem = 'teste da minha aula de python'

            kit.sendwhatmsg_instantly(numero_destino,mensagem,wait_time=40)
            print ('Whats enviado')

        except Exception as e:
            print (f'Erro:{e}')


start = toDo()
start.iniciar()
