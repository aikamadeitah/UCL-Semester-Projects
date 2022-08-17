# mqtt-to-db

Microservice that reads mqtt messages from a broker and stores them in a mongodb collection.

If you need a client to publish data, an example is here: https://gitlab.com/21s-itt2-datacenter-students-group/examples/mqtt-tests 

1. Complete the mongodb/atlas guide https://docs.atlas.mongodb.com/tutorial/create-atlas-account/
2. Clone the repository `git clone git@gitlab.com:21s-itt2-datacenter-students-group/examples/mqtt-to-db.git` 
3. Create a virtual environment https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment 
4. Activate the virtual environment https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#activating-a-virtual-environment
5. Install requirements from requirements.txt https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#using-requirements-files
6. Create a file called `token.txt` and insert your mongodb/atlas password see: https://docs.atlas.mongodb.com/tutorial/create-mongodb-user-for-cluster/#set-the-new-user-s-username-and-password for details
7. Format and replace `connection_string` with your mongodb/atlas connection string
8. Run `python3 mqtt-to-db.py` (linux) or `py mqtt-to-db.py` (windows)

Troubleshooting:

1. Make sure your broker is running
2. Make sure you are publishing to the broker from a client

Ressources:

* Pymongo docs https://pymongo.readthedocs.io/en/stable/index.html
* Paho-mqtt docs https://pypi.org/project/paho-mqtt/