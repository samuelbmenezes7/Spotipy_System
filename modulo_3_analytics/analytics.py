import pika
import json
import datetime
from colorama import init, Fore, Style
import pyfiglet

init()

RABBITMQ_URL = 'amqps://odxnwdwz:ud16l2oiHhUDEqOOISGgOcTm9jvv2Lum@jackal.rmq.cloudamqp.com/odxnwdwz'

# Filas v2
FILA_HISTORICO = 'fila_historico_v2'

print(pyfiglet.figlet_format("ANALYTICS"))
print("--------------------------------------------------")

def registrar_historico(ch, method, properties, body):
    dados = json.loads(body)
    agora = datetime.datetime.now().strftime("%H:%M:%S")
    
    print(f"{Fore.GREEN}✓ [SUCESSO]{Style.RESET_ALL} {agora} | {Fore.CYAN}{dados['usuario']}{Style.RESET_ALL} ouviu {Fore.YELLOW}{dados['musica']}{Style.RESET_ALL}")
    
    with open('historico_play.txt', 'a', encoding='utf-8') as f:
        f.write(f"[{agora}] User: {dados['usuario']} | Music: {dados['musica']}\n")
        
    ch.basic_ack(delivery_tag=method.delivery_tag)

params = pika.URLParameters(RABBITMQ_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue=FILA_HISTORICO)
channel.basic_consume(queue=FILA_HISTORICO, on_message_callback=registrar_historico)

print(f"{Fore.MAGENTA} [*] Aguardando logs na fila '{FILA_HISTORICO}'...{Style.RESET_ALL}")
channel.start_consuming()