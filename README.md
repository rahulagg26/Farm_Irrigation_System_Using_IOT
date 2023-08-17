# Farm_Irrigation_System_Using_IOT
The programme to display the value of the sensors, which is mentioned below:

import RPi.GPIO as GPIO
import dht11
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
# read data using pin 14
instance = dht11.DHT11(pin = 17)
result = instance.read()
if result.is_valid():
    print("Temperature: %-3.1f C" % result.temperature)
    print("Humidity: %-3.1f %%" % result.humidity)
else:
    print("Error: %d" % result.error_code)


As per our implementation, we have created three python files to establish the required communication between the system and the Raspberry Pi. The use of three different python files is illustrated below:

•subscriber.py: This file is present on our system (laptop), where in the first case we are acting as a subscriber, and in the second case we are acting as a publisher. This file contains the below mentioned code:

1.	import paho.mqtt.client as mqtt
2.	def on_connect(client, userdata, flags, rc):
3.	
4.	    print(f"Connected with result code {rc}")
5.	    client.subscribe("raspberry/topic")
6.	
7.	def on_message(client, userdata, msg):
8.	    print(f"{msg.payload}")
9.	    
10.	    publish(client,msg)
11.	
12.	def publish(client,msg):
13.	    
14.	    client.publish("topic",payload=f"{msg.payload}", qos=0, retain=False)
15.	
16.	client_s = mqtt.Client()
17.	client_s.on_connect = on_connect
18.	client_s.on_message = on_message
19.	client_s.enable_bridge_mode()
20.	
21.	client_s.will_set('raspberry/status', b'{"status": "Off"}')
22.	
23.	client_s.connect("test.mosquitto.org", 1883, 60)
24.	
25.	client_s.loop_forever()

•publisher.py: This file is present on our Raspberry Pi, where we are publishing the temperature and humidity values. This file contains the below mentioned code:

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


•subscriber.py: This file is also present on our Raspberry Pi where we are acting as a subscriber to receive the predicted value of water percentage from the publisher with the help of an ML model. This file contains the below mentioned code:

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("topic")

def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.will_set('raspberry/status', b'{"status": "Off"}')
client.connect("test.mosquitto.org", 1883, 60)
client.loop_forever()


Eventually, to display the predicted water percentage in LCD, which is calculated via the ML Model, we have designed the code as shown below with the required configuration.

import time
import Adafruit_CharLCD as LCD

# Raspberry Pi pin configuration:
lcd_rs        = 12  
lcd_en        = 7
lcd_d4        = 8
lcd_d5        = 25
lcd_d6        = 17
lcd_d7        = 23
lcd_backlight = 4

lcd_columns = 20
lcd_rows    = 4

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

lcd.message('Hello\nworld!')

time.sleep(5.0)

# Demo showing the cursor.
lcd.clear()
lcd.show_cursor(True)
lcd.message('Show cursor')

time.sleep(5.0)

# Demo showing the blinking cursor.
lcd.clear()
lcd.blink(True)
lcd.message('Blink cursor')

time.sleep(5.0)

# Stop blinking and showing cursor.
lcd.show_cursor(False)
lcd.blink(False)

# Demo scrolling message right/left.
lcd.clear()
message = 'Scroll'
lcd.message(message)
for i in range(lcd_columns-len(message)):
    time.sleep(0.5)
    lcd.move_right()
for i in range(lcd_columns-len(message)):
    time.sleep(0.5)
    lcd.move_left()

# Demo turning backlight off and on.
lcd.clear()
lcd.message('Flash backlight\nin 5 seconds...')
time.sleep(5.0)
# Turn backlight off.
lcd.set_backlight(0)
time.sleep(2.0)
# Change message.
lcd.clear()
lcd.message('Goodbye!')
# Turn backlight on.
lcd.set_backlight(1)

The below code is implemented to train and to find the accuracy of the model:

import numpy as np
from sklearn.model_selection import train_test_split
import sklearn
from sklearn.svm import LinearSVC

from pandas import read_csv
import pandas as pd
data = read_csv( "IOT_Assignment_2_data_regression_sensor_range.csv" )
x=data.loc[:,"Humidity(%)"]
y=data.loc[:,"Temperature(°C)"]
z=data.loc[:,"WaterFlow(%)"]
x = data[["Humidity(%)", "Temperature(°C)", "WaterFlow(%)"]]
X = x[["Humidity(%)", "Temperature(°C)"]]
Y = x["WaterFlow(%)"]
X_train, X_test, y_train, y_test = train_test_split(X, Y,test_size=0.3,train_size=0.7, random_state = 0)

from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

model = linear_model.LinearRegression()

model.fit(X_train, y_train)
# predict
y_pred = model.predict(X_test)

# model evaluation
score = r2_score(y_test, y_pred)
print(score)
