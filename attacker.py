import paho.mqtt.client as mqtt
import random

broker = "127.0.0.1"

subscribe_topic = "test"
publish_topic = "test_attack"

def on_connect(client, userdata, flags, rc):
    client.subscribe(subscribe_topic)

def on_message(client, userdata, msg):

    received = msg.payload.decode()

    try:
        data_string, received_hash = received.split("|")
    except:
        data_string = received

    values = data_string.split(",")

    # modify realistic numeric field
    indexes = [1,3,8,9,10,11,12,13]
    index = random.choice(indexes)

    values[index] = str(float(values[index]) + random.randint(5,40))

    tampered_data = ",".join(values)

    # IMPORTANT: do NOT send hash again
    client.publish(publish_topic, tampered_data)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker,1883)

print("Listening...")

client.loop_forever()