from fastapi import FastAPI, WebSocket
import pika
import json

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='prediction_results')

    for method_frame, properties, body in channel.consume('prediction_results'):
        await websocket.send_text(body.decode())
        channel.basic_ack(method_frame.delivery_tag)
        break
