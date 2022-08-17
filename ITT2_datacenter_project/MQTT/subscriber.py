#!/usr/bin/env/ python 3
import paho.mqtt.client as mqtt

brokerIP = "xxx.xxx.x.xx" #Input the corresponding IP Addresse/Domain name for the broker
brokerPort = 1883 #Input the broker Port
brokerKeepAlive = 60
myTopic = "plant1/temp" #Input the subscriber topic

def on_connect(client, userdata, flags, rc):
	#print("Connected with code" + str(rc)) #Uncomment this code for connection confirmations output to terminal
	client.subscribe(myTopic)

def message(client, userdata, msg):
	print("Fetched: " + str(msg.payload.decode())+" from topic " + myTopic)
	client.disconnect()

client = mqtt.Client()
client.connect(brokerIP, brokerPort, brokerKeepAlive)
client.on_connect = on_connect
client.on_message = message
client.loop_forever()
