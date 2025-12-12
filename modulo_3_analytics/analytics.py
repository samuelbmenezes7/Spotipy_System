import pika
import json
import datetime
from colorama import init, Fore, Style # Importa cores

# Inicializa as cores no Windows
init()

RABBITMQ_URL = 'amqps://odxnwdwz:ud16l2oiHhUDEqOOISGgOcTm9jvv2Lum@jackal.rmq.cloudamqp.com/odxnwdwz'

def registrar_historico(ch, method, properties, body):
    dados = json.loads(body)
    agora = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Imprime COLORIDO na tela
    print(f"{Fore.GREEN}✓ [SUCESSO]{Style.RESET_ALL} {agora} | {Fore.CYAN}{dados['usuario']}{Style.RESET_ALL} ouviu {Fore.YELLOW}{dados['musica']}{Style.RESET_ALL}")
    
    with open('historico_play.txt', 'a', encoding='utf-8') as f:
        f.write(f"[{agora}] User: {dados['usuario']} | Music: {dados['musica']}\n")
        
    ch.basic_ack(delivery_tag=method.delivery_tag)

params = pika.URLParameters(RABBITMQ_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='fila_historico')
channel.basic_consume(queue='fila_historico', on_message_callback=registrar_historico)

print(f"{Fore.MAGENTA} [*] SPOTIPY ANALYTICS DATA WAREHOUSE - Online{Style.RESET_ALL}")
channel.start_consuming()