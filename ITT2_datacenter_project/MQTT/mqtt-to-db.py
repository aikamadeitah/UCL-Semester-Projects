'''
A small pyhton application that receives MQTT messages, in JSON format, from a broker and inserts the messages 
into a mongodb collection hosted on atlas: https://www.mongodb.com/cloud/atlas

see README.md for setup and usage instructions

Authors: Mathias Gregersen & Nikolaj Simonsen
'''

import paho.mqtt.client as mqtt
import pymongo
import json
from socket import error as socket_error
import functions

# replace with valid broker and port
mqtt_broker_addr = 'duckmqttduck.northeurope.cloudapp.azure.com'
mqtt_broker_port = 1883

# init mqtt client
client = mqtt.Client() # init mqtt client

# replace with valid topic
topic = 'rpi1/number'

# read token from token.txt file containing the mongodb password 
# see: https://docs.atlas.mongodb.com/tutorial/create-mongodb-user-for-cluster/#set-the-new-user-s-username-and-password
token = functions.get_token('token.txt')

# replace with your cluster connection string, format it according to the example shown 
# see: https://docs.atlas.mongodb.com/tutorial/connect-to-your-cluster/#connect-to-your-atlas-cluster 
connection_string = 'mongodb+srv://New_User:' + token + '@duckcluster.eko3s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

# init pymongo client
db_client = pymongo.MongoClient(connection_string)
# database (will be created at first connect to atlas)
db = db_client.mqtt_test
# collection (will be created at first connect to atlas)
db_collection = db.sensor

# triggers when connected to mqtt broker
def on_connect(client, userdata, flags, rc):
    print(f'connected to {mqtt_broker_addr} on port {mqtt_broker_port}')
   
# triggers when message received from broker
def on_message(client, userdata, msg):
    document = json.loads(msg.payload) # create a dictionary from MQTT received message
    print(f'attempting db store: {document}') # print the document for development purposes
    return_id = db_collection.insert_one(document) # insert the document in the database
    print(f'stored in db with _id: {return_id.inserted_id}') # print the returned document _id from the database

# attach callbacks
client.on_connect = on_connect
client.on_message = on_message

try: 
    print('connecting to broker')
    client.connect(mqtt_broker_addr, mqtt_broker_port) # connect to mqtt broker
    client.subscribe(topic) # subscribe to topic
    print(f'subscribed to topics: {topic}')
    client.loop_start() # start receiving mqtt messages

except socket_error as e:
    print(f'could not connect to {mqtt_broker_addr} on port {mqtt_broker_port}\n {e}')
    exit(0)

while True:
    try:
        pass
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop() #stop the loop
        exit(0)
