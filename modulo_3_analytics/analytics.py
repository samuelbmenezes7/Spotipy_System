import pika
import json
import datetime

RABBITMQ_URL = 'amqps://odxnwdwz:ud16l2oiHhUDEqOOISGgOcTm9jvv2Lum@jackal.rmq.cloudamqp.com/odxnwdwz'

def registrar_historico(ch, method, properties, body):
    dados = json.loads(body)
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[Analytics] 💾 Salvando registro: {dados['musica']} - {agora}")
    
    with open('historico_play.txt', 'a', encoding='utf-8') as f:
        f.write(f"[{agora}] Usuário: {dados['usuario']} | Ouviu: {dados['musica']}\n")
        
    ch.basic_ack(delivery_tag=method.delivery_tag)

params = pika.URLParameters(RABBITMQ_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='fila_historico')
channel.basic_consume(queue='fila_historico', on_message_callback=registrar_historico)

print(" [*] Módulo ANALYTICS aguardando dados...")
channel.start_consuming()