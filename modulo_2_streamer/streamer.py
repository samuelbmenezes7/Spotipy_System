import pika
import json
import time
from tqdm import tqdm
import pyfiglet

# SEU URL
RABBITMQ_URL = 'amqps://odxnwdwz:ud16l2oiHhUDEqOOISGgOcTm9jvv2Lum@jackal.rmq.cloudamqp.com/odxnwdwz'

# Filas v2 (Novas e Vazias)
FILA_TOCADOR = 'fila_tocador_v2'
FILA_HISTORICO = 'fila_historico_v2'

# Banner inicial
print(pyfiglet.figlet_format("STREAMER  v2.0"))
print("--------------------------------------------------")

def processar_musica(ch, method, properties, body):
    dados = json.loads(body)
    musica = dados['musica']
    # Garante que vai usar o tempo rápido enviado pelo app.py (5s)
    duracao = dados.get('duracao_simulada', 5) 
    artista = dados['artista']
    
    print(f"\n[Streamer] 📥 Pedido recebido: {musica} - {artista}")
    
    # BARRA DE PROGRESSO DE TEMPO (RÁPIDA)
    with tqdm(total=100, desc=f"🎵 Processando", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}%", colour='green') as pbar:
        passo = duracao / 100
        for _ in range(100):
            time.sleep(passo)
            pbar.update(1)
    
    msg_analytics = {'musica': musica, 'status': 'tocada', 'usuario': dados['usuario']}
    
    channel.basic_publish(exchange='', routing_key=FILA_HISTORICO, body=json.dumps(msg_analytics))
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

params = pika.URLParameters(RABBITMQ_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Declara as filas novas
channel.queue_declare(queue=FILA_TOCADOR)
channel.queue_declare(queue=FILA_HISTORICO)

# Isso garante que ele só pegue UMA música por vez e não trave
channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue=FILA_TOCADOR, on_message_callback=processar_musica)

print(f" [*] Conectado na fila '{FILA_TOCADOR}' - Aguardando tarefas...")
channel.start_consuming()