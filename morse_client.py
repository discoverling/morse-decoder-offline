import random
import time
from paho.mqtt import client as mqtt_client

# Decoder settings
intraCharacterPause = 0.5
timeout_period = 1.5
char_count = 0
button_time = 0
new_char_received = False

# MQTT settings
client_id = f'publish-{random.randint(0, 1000)}'

def connect_mqtt(broker, port):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 5:
            break

def disconnect(client):
    client.loop_stop()
    client.disconnect()
    time.sleep(0.1)

def subscribe(client: mqtt_client, topic):    
    client.subscribe(topic)
    client.on_message = on_message

def loop_start(client):
    client.loop_start()
    
def on_message(client, userdata, msg):
    global char_count
    global button_time
    global new_char_received
    new_char_received = True
    button_time = int(msg.payload.decode())
    char_count += 1
    # print(f"Received `{button_time}` from `{msg.topic}` topic")

def decode_morse(classifier, classmap): 
    global char_count
    global button_time
    global new_char_received
    last_received_time = 0
    char_array = [0, 0, 0, 0]
    
    while True:   
        current_time = time.time()   
        if new_char_received:
            if char_count > 0: 
                if char_count == 1:
                    last_received_time = current_time
                if current_time - last_received_time - button_time < intraCharacterPause:
                    char_array[char_count-1] = button_time 
                    last_received_time = current_time  # Update the timestamp
                else:
                    char_count = 4                
            if char_count == 4:
                class_prediction = classifier.predict([char_array])
                print("{} ".format(classmap[class_prediction[0]]))
                char_count = 0
                char_array = [0, 0, 0, 0]
            new_char_received = False
        else:
            # Check for timeout event when no new characters were received in time
            if current_time - last_received_time > timeout_period and char_count > 0: 
                char_count = 0 # Reached end of character
                class_prediction = classifier.predict([char_array])
                print("{} ".format(classmap[class_prediction[0]]))
        time.sleep(0.2)