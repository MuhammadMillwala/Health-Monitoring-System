import joblib
import pika
import json
import time

def load_model():
    return joblib.load('/app/random_forest_heart_disease_model.pkl')

def callback(ch, method, properties, body):
    model = load_model()
    data = json.loads(body)
    prediction = model.predict([list(data.values())])
    result = {"prediction": int(prediction[0])}
    publish_prediction_result(result)

def publish_prediction_result(result):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='prediction_results')
    channel.basic_publish(exchange='', routing_key='prediction_results', body=json.dumps(result))
    connection.close()

def connect_to_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print('Failed to connect to RabbitMQ. Retrying in 5 seconds...')
            time.sleep(5)

connection = connect_to_rabbitmq()
channel = connection.channel()
channel.queue_declare(queue='health_data')
channel.basic_consume(queue='health_data', on_message_callback=callback, auto_ack=True)
print('Waiting for messages...')
channel.start_consuming()
