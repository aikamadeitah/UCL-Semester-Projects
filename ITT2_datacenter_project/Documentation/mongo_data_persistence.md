PART 1 - MONGODB
	- Deploy a Free Tier Cluster. The following link should be able to guide you through this. (https://docs.atlas.mongodb.com/getting-started/)
	
PART 2 - MQTT to MONGODB
	- Clone this repository (https://gitlab.com/21s-itt2-datacenter-students-group/examples/mqtt-to-db) and follow the directions in the readme file.
	- Once that is accomplished, publish some data to the topic where MQTT-to-DB is subscribed. You can use your own publisher or the test client found in the repository from the previous step.
	- Check your MongoDB collection to see that it is picking up the information that is being sent by your publisher.
	
PART 3 - AZURE CLOUDS
	- Create a Virtual Machine for your MQTT to DB app on Azure.[You should use Debian 10 "Buster" with Gen1 backports kernel and a standard B1 machine size (1VCPU,1GiBm memory] (You can follow this guide if you don't know how to make an Azure VM (https://docs.microsoft.com/en-us/azure/virtual-machines/linux/quick-create-portal))
	- With Azure, set up a Virtual Network for your broker and MQTT-to-DB VMs and use their corresponding private IP in your MWTT-to-DB application OR configure a network inbound rule for the MQTT broker VM to allow for connections
	- In Atlas, add the public IP of the mqtt-to-db vm to the IP Access List
	-Clone the mqtt-db from the previous step to the VM
	
PART 4 - TESTING THE THING
	- Start everything (That is, the MQTT Azure broker microservice, the MQTT-to-DB Azure microservice and your client to sent information from a sensor to the MQTT Broker.
	- After everything is running, check that the Mongo Atlas has the data that you've sent.
