#  Spotipy - Sistema Distribuído de Streaming

Projeto desenvolvido para a disciplina de Sistemas Distribuídos. O sistema simula uma arquitetura de streaming de áudio desacoplada, utilizando filas de mensagens para processamento assíncrono.

##  Arquitetura

O sistema utiliza o padrão **Publisher/Subscriber** com **RabbitMQ**:

1.  **Módulo 1 (Client/Frontend):** Interface Web em Flask. Atua como *Producer*, enviando solicitações de música e servindo os arquivos de áudio via rede local.
2.  **Módulo 2 (Streamer Worker):** Atua como *Consumer*. Recebe a tarefa, verifica a integridade do arquivo (simulação de buffer) e processa a execução.
3.  **Módulo 3 (Analytics Worker):** Atua como *Logger*. Registra o histórico de reprodução e gera logs de auditoria.

##  Tecnologias

* **Linguagem:** Python 3.x
* **Web Framework:** Flask
* **Middleware:** RabbitMQ (AMQP)
* **Bibliotecas:** Pika, TQDM, Colorama

##  Como Rodar

1.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

2.  Inicie os módulos em terminais separados:

    * **Terminal 1 (Interface):**
        ```bash
        cd modulo_1_client
        python app.py
        ```
    * **Terminal 2 (Streamer):**
        ```bash
        cd modulo_2_streamer
        python streamer.py
        ```
    * **Terminal 3 (Analytics):**
        ```bash
        cd modulo_3_analytics
        python analytics.py
        ```

3.  Acesse `http://localhost:5000` (ou via IP no celular).

##  Equipe
* Samuel - Desenvolvedor Full Stack