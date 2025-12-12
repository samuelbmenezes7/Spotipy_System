from flask import Flask, render_template, request, jsonify
import pika
import json
import datetime
import os

app = Flask(__name__)

# SEU URL DO RABBITMQ
RABBITMQ_URL = 'amqps://odxnwdwz:ud16l2oiHhUDEqOOISGgOcTm9jvv2Lum@jackal.rmq.cloudamqp.com/odxnwdwz'

# Filas v2
FILA_TOCADOR = 'fila_tocador_v2' 
FILA_HISTORICO = 'fila_historico_v2'

# CATÁLOGO
MUSICAS = [
    {
        'id': '1', 'titulo': 'Bohemian Rhapsody', 'artista': 'Queen', 
        'duracao': 355, 'genero': 'Rock', 'views': 1500000,
        'capa': 'https://upload.wikimedia.org/wikipedia/en/9/9f/Bohemian_Rhapsody.png', 'arquivo': 'bohemian.mp3' 
    },
    {
        'id': '2', 'titulo': 'Shape of You', 'artista': 'Ed Sheeran', 
        'duracao': 233, 'genero': 'Pop', 'views': 2300000,
        'capa': 'https://upload.wikimedia.org/wikipedia/en/4/45/Divide_cover.png', 'arquivo': 'shape.mp3'
    },
    {
        'id': '3', 'titulo': 'Hotel California', 'artista': 'Eagles', 
        'duracao': 390, 'genero': 'Rock', 'views': 900000,
        'capa': 'https://upload.wikimedia.org/wikipedia/en/4/49/Hotelcalifornia.jpg', 'arquivo': 'hotel.mp3'
    },
    {
        'id': '4', 'titulo': 'Blinding Lights', 'artista': 'The Weeknd', 
        'duracao': 200, 'genero': 'Pop', 'views': 1800000,
        'capa': 'https://upload.wikimedia.org/wikipedia/en/e/e6/The_Weeknd_-_Blinding_Lights.png', 'arquivo': 'blinding.mp3'
    }
]

def enviar_para_fila(mensagem):
    try:
        params = pika.URLParameters(RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=FILA_TOCADOR)
        channel.basic_publish(exchange='', routing_key=FILA_TOCADOR, body=json.dumps(mensagem))
        connection.close()
    except Exception as e:
        print(f"Erro RabbitMQ: {e}")

@app.route('/')
def index():
    termo_busca = request.args.get('q', '').lower()
    
    if termo_busca:
        resultados = [m for m in MUSICAS if termo_busca in m['titulo'].lower() or termo_busca in m['artista'].lower()]
        return render_template('index.html', secoes={'🔍 Resultados da Busca': resultados}, busca=termo_busca)

    # Lógica das Seções
    mais_tocadas = sorted(MUSICAS, key=lambda x: x['views'], reverse=True)[:4]
    rock = [m for m in MUSICAS if m['genero'] == 'Rock']
    pop = [m for m in MUSICAS if m['genero'] == 'Pop']

    secoes = {
        '🔥 Mais Tocadas': mais_tocadas,
        '🎸 Rock Clássico': rock,
        '🎉 Pop Hits': pop
    }

    return render_template('index.html', secoes=secoes, busca='')

@app.route('/api/trigger_play', methods=['POST'])
def trigger_play():
    data = request.json
    musica_id = data.get('id')
    # AQUI: Pega o usuário que veio do HTML. Se não vier, usa 'Anônimo'
    nome_usuario = data.get('usuario', 'Anônimo') 
    
    musica = next((m for m in MUSICAS if m['id'] == musica_id), None)
    
    if musica:
        msg = {
            'musica': musica['titulo'],
            'artista': musica['artista'],
            'duracao_simulada': 5, 
            'usuario': nome_usuario, # Usa o nome dinâmico
            'timestamp': str(datetime.datetime.now())
        }
        enviar_para_fila(msg)
        return jsonify({"status": "enviado"})
    return jsonify({"status": "erro"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)