import pika
import json
import time

RABBITMQ_URL = 'amqps://odxnwdwz:ud16l2oiHhUDEqOOISGgOcTm9jvv2Lum@jackal.rmq.cloudamqp.com/odxnwdwz'

def processar_musica(ch, method, properties, body):
    dados = json.loads(body)
    musica = dados['musica']
    duracao = dados['duracao_simulada']
    
    print(f"\n[Streamer] 📥 Recebido pedido: {musica}")
    print(f"[Streamer] 🎵 Tocando... (Aguarde {duracao}s)")
    time.sleep(duracao)
    print(f"[Streamer] ✅ Música finalizada!")

    msg_analytics = {'musica': musica, 'status': 'tocada', 'usuario': dados['usuario']}

    channel.basic_publish(exchange='', routing_key='fila_historico', body=json.dumps(msg_analytics))
    print(f"[Streamer] 📤 Dados enviados para o Analytics.")
    ch.basic_ack(delivery_tag=method.delivery_tag)

params = pika.URLParameters(RABBITMQ_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='fila_tocador')
channel.queue_declare(queue='fila_historico')
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='fila_tocador', on_message_callback=processar_musica)

print(" [*] Módulo STREAMER aguardando músicas...")
channel.start_consuming()