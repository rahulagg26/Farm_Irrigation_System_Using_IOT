import paho.mqtt.client as mqtt
def on_connect(client, userdata, flags, rc):
	
    print(f"Connected with result code {rc}")
    client.subscribe("raspberry/topic")
	
def on_message(client, userdata, msg):
    print(f"{msg.payload}")
    
    publish(client,msg)
	
def publish(client,msg):
	    
    client.publish("topic",payload=f"{msg.payload}", qos=0, retain=False)
	
    client_s = mqtt.Client()
    client_s.on_connect = on_connect
    client_s.on_message = on_message
    client_s.enable_bridge_mode()
    client_s.will_set('raspberry/status', b'{"status": "Off"}')
    client_s.connect("test.mosquitto.org", 1883, 60)
    client_s.loop_forever()