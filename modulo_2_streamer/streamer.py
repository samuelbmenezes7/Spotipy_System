import pika
import json
import time
from tqdm import tqdm # Importa a barra de progresso

RABBITMQ_URL = 'amqps://odxnwdwz:ud16l2oiHhUDEqOOISGgOcTm9jvv2Lum@jackal.rmq.cloudamqp.com/odxnwdwz'

def processar_musica(ch, method, properties, body):
    dados = json.loads(body)
    musica = dados['musica']
    duracao = dados['duracao_simulada']
    artista = dados['artista']
    
    print(f"\n[Streamer] 📥 Pedido recebido: {musica} - {artista}")
    
    # BARRA DE PROGRESSO VISUAL
    with tqdm(total=100, desc=f"🎵 Tocando", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}%", colour='green') as pbar:
        passo = duracao / 100
        for _ in range(100):
            time.sleep(passo)
            pbar.update(1)
    
    msg_analytics = {'musica': musica, 'status': 'tocada', 'usuario': dados['usuario']}
    channel.basic_publish(exchange='', routing_key='fila_historico', body=json.dumps(msg_analytics))
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

params = pika.URLParameters(RABBITMQ_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='fila_tocador')
channel.queue_declare(queue='fila_historico')
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='fila_tocador', on_message_callback=processar_musica)

print(" [*] SPOTIPY STREAMER (Engine v2.0) - Aguardando...")
channel.start_consuming()