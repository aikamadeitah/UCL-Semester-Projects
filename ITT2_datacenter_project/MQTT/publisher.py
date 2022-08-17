import paho.mqtt.client as mqtt

broker_address="test.mosquitto.org"
client = mqtt.Client("P1")
client.connect(broker_address)
client.publish("RNG", "17")