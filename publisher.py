import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
import dht11

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 14
instance = dht11.DHT11(pin = 17)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code sfasf {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect("test.mosquitto.org", 1883, 60)

while True:
    result = instance.read()
    client.publish('raspberry/topic', payload=f" temp:{result.temperature} humidity:{result.humidity} ", qos=0, retain=False)
    print(f"send  temp:{result.temperature} humidity:{result.humidity} to raspberry/topic")
    time.sleep(5)

client.loop_forever()