from flask import Flask, render_template, request, redirect, url_for, flash
import pika
import json
import datetime

app = Flask(__name__)
app.secret_key = 'segredo_rapido'

# SEU URL DO RABBITMQ
RABBITMQ_URL = 'amqps://odxnwdwz:ud16l2oiHhUDEqOOISGgOcTm9jvv2Lum@jackal.rmq.cloudamqp.com/odxnwdwz'

# Catálogo Fictício
MUSICAS = {
    '1': {'titulo': 'Bohemian Rhapsody', 'artista': 'Queen', 'duracao': 5},
    '2': {'titulo': 'Shape of You', 'artista': 'Ed Sheeran', 'duracao': 3},
    '3': {'titulo': 'Hotel California', 'artista': 'Eagles', 'duracao': 4}
}

def enviar_para_fila(mensagem):
    try:
        params = pika.URLParameters(RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue='fila_tocador')
        
        channel.basic_publish(exchange='',
                              routing_key='fila_tocador',
                              body=json.dumps(mensagem))
        connection.close()
    except Exception as e:
        print(f"Erro ao conectar no RabbitMQ: {e}")

@app.route('/')
def index():
    return render_template('index.html', musicas=MUSICAS)

@app.route('/play/<id>')
def play(id):
    musica = MUSICAS.get(id)
    if musica:
        msg = {
            'musica': musica['titulo'],
            'artista': musica['artista'],
            'duracao_simulada': musica['duracao'],
            'usuario': 'Samuel',
            'timestamp': str(datetime.datetime.now())
        }
        enviar_para_fila(msg)
        flash(f"Solicitação enviada: {musica['titulo']}")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)