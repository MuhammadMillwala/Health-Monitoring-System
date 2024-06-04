from fastapi import APIRouter
from pydantic import BaseModel
import pika
import json

router = APIRouter()

class HealthData(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

def send_to_queue(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='health_data')
    channel.basic_publish(exchange='', routing_key='health_data', body=json.dumps(data))
    connection.close()

@router.post("/predict")
async def predict(data: HealthData):
    send_to_queue(data.dict())
    return {"message": "Data sent for processing"}
