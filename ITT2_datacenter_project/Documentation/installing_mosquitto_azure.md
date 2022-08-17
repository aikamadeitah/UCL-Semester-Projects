# Installing Mosquitto on Azure

* Introduction
* Problem encountered following the guide
    * Gnupg not installed
    * Broken repository
* Modified Guide
    * Add the Mosquitto Debian repository
    * Install Mosquitto and its command line clients
    * Check it’s running
    * Test that it’s working
    * Adding Websocket protocol support

---
## Introduction

While setting up Mosquitto on the azure VM, errors was encountered while following the guide provided in the exercises.

Here is how i got around it and made it work.

---
## Problem encountered following the guide

Error encountered while installing mosquitto following guide

[Guide](https://medium.com/@rossdanderson/installing-mosquitto-broker-on-debian-2a341fe88981)

## Gnupg not installed

```
E: gnupg, gnupg2 and gnupg1 do not seem to be installed, but one of them is required for this operation
```

### Fix

    apt-get update
    apt-get install gnupg

> *This is as simple as just installing the gnupg packages*



## Broken repository

```
sudo apt-get install mosquitto
Reading package lists... Done
Building dependency tree       
Reading state information... Done
Some packages could not be installed.
This may mean that you have requested an impossible situation or if you are using the unstable 
distribution that some required packages have not yet been created or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies:
 mosquitto : Depends: libssl1.0.0 (>= 1.0.0) but it is not installable
E: Unable to correct problems, you have held broken packages.

```
### Fix

Changed

    sudo wget http://repo.mosquitto.org/debian/mosquitto-jessie.list

> *This list is ment for the Debian 8 code named Jessie*

To

    sudo wget http://repo.mosquitto.org/debian/mosquitto-buster.list
    
> *Because we are using Debian 10(Buster) the list should be directed to buster instead*

If you already downloaded the jessie repo list you will likely have to remove it for the install to work, otherwise it will still look in the jessie repo before checking in the buster repo, and post the same error.

---

# Modified Guide

## Add the Mosquitto Debian repository

Add the Mosquitto Debian repository

    wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
    sudo apt-key add mosquitto-repo.gpg.key

    cd /etc/apt/sources.list.d/

    sudo wget http://repo.mosquitto.org/debian/mosquitto-buster.list
    sudo apt-get update

> If when doing these steps you get and message about gnupg not being installed, just install gnupg from the repository.

## Install Mosquitto and its command line clients

    sudo apt-get install mosquitto

    sudo apt-get install mosquitto-clients

## Check it’s running

    sudo service mosquitto status


### What you want to see is something like

```
● mosquitto.service - Mosquitto MQTT Broker
   Loaded: loaded (/lib/systemd/system/mosquitto.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2021-02-22 11:42:20 UTC; 10min ago
     Docs: man:mosquitto.conf(5)
           man:mosquitto(8)
 Main PID: 14409 (mosquitto)
    Tasks: 1 (limit: 4113)
   Memory: 976.0K
   CGroup: /system.slice/mosquitto.service
           └─14409 /usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf

Feb 22 11:42:20 myVM systemd[1]: Starting Mosquitto MQTT Broker...
Feb 22 11:42:20 myVM systemd[1]: Started Mosquitto MQTT Broker.
```
### To start, stop and restart the broker in future, use the commands
    
    sudo service mosquitto start
    sudo service mosquitto stop
    sudo service mosquitto restart
    
## Test that it’s working

In your existing terminal, subscribe to the “testtopic” topic

    mosquitto_sub -h localhost -t "testtopic" -v

Then open another terminal and send a message on that topic

    mosquitto_pub -h localhost -t "testtopic" -m "Testing"

If all goes well then should see the message printed to the first terminal

    chip@chip:~$ mosquitto_sub -h localhost -t "testtopic" -v
    testtopic Testing

Success! You have a working MQTT broker running on the default port 1883.

## Adding Websocket protocol support

> This section is not part of the Exersices

Currently we only have MQTT protocol, so to enable Websockets on port 1884, we need to configure and restart Mosquitto. To do this, start by creating a configuration file in the appropriate location. 
I’ve called mine protocols.conf.

    sudo vi /etc/mosquitto/conf.d/protocols.conf

> Here we are using VIM to create and edit the file, if you are unfamiliar with VIM here is a site with some guidens. [Vim commands](https://linuxhandbook.com/basic-vim-commands/)

Define the contents like so

    listener 1883
    protocol mqtt

    listener 1884
    protocol websockets

And again, restart with

    sudo service mosquitto restart
