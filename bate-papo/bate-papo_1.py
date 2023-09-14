# pip install pika --upgrade
import pika
import time
from threading import Thread
from tkinter import *
from tkinter import messagebox


credentials = pika.PlainCredentials("chat_1", "chat_1")


def receptor():

    def chamada(ch, method, propreties, body):
        mensagens.insert(END, "Ele(a):  " + body.decode())

    conexao = pika.BlockingConnection(
        pika.ConnectionParameters("127.0.0.1", 5672, "/", credentials))

    canal = conexao.channel()
    canal.queue_declare(queue="fila_2")

    if (canal.basic_consume(queue="fila_2", on_message_callback=chamada, auto_ack=True)):
        mensagens.insert(END, "Um momento... ")
        time.sleep(2)
        messagebox.showinfo("Mensageiro", "O bate-papo está ativo!")
        mensagens.delete(0, END)

    canal.start_consuming()
    conexao.close()


def envio():

    conexao = pika.BlockingConnection(
        pika.ConnectionParameters("127.0.0.1", 5672, "/", credentials))

    canal = conexao.channel()
    canal.queue_declare(queue="fila_1")

    live = entrada.get()
    mensagens.insert(END, "Você:  " + live)

    canal.basic_publish(exchange="", routing_key="fila_1", body=live)
    conexao.close()


def limpar():
    mensagens.delete(0, END)


def apagar(entrada):
    entrada.delete(0, END)


janela = Tk()
janela.title("Mensageiro")
janela.state("zoomed")
janela.configure(bg="#003884")


rotulo = Label(text="Mensageiro", font=(
    "Roboto", 32, "bold"), fg="#ffffff", bg="#003884", pady=16)
rotulo.pack()


quadro = Frame(janela)

barra_lateral = Scrollbar(quadro)

mensagens = Listbox(quadro, height=16, width=64,
                    yscrollcommand=barra_lateral.set, font=("Roboto", 16, "bold"), fg="#ff6600")
barra_lateral.pack(side=RIGHT, fill=Y)

mensagens.pack(side=LEFT, fill=BOTH)

quadro.pack()


quadro_acoes = Frame(janela, bg="#003884", pady=16)

texto_quadro = Label(quadro_acoes, text="Digite sua mensagem: ", font=(
    "Roboto", 16, "bold"), bg="#003884", fg="#ffffff")
texto_quadro.pack(side=LEFT, anchor=CENTER, padx=8)

entrada = Entry(quadro_acoes, textvariable="",
                font=("Roboto", 16, "bold"), fg="#003884")
entrada.pack(side=LEFT, anchor=CENTER, padx=8)

botao_enviar = Button(quadro_acoes, text="Enviar", command=envio,
                      bg="#ff6600", font=("Roboto", 16, "bold"), fg="#ffffff")
botao_enviar.pack(side=LEFT, anchor=CENTER, padx=8)

botao_apagar = Button(quadro_acoes, text="Apagar Texto", command=lambda: apagar(
    entrada), font=("Roboto", 16, "bold"), fg="#003884")
botao_apagar.pack(side=LEFT, anchor=CENTER, padx=8)

quadro_acoes.pack()


botao_limpar = Button(text="Limpar Tela", command=limpar,
                      bg="#ffffff", font=("Roboto", 16, "bold"), fg="#ff6600")
botao_limpar.pack(anchor=CENTER, pady=16)


receive_thread = Thread(target=receptor)
envio_thread = Thread(target=envio)

receive_thread.start()
envio_thread.start()


janela.mainloop()
