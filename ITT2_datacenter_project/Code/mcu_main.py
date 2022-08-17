import network
import socket
import time
import dht
from machine import Pin

APIKEY = '83EYR1R3FZHMV94R'
WriteChId = '1390216'

#
# This function connects to the Wi-Fi
#
def Connect_WiFi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(self.ssid, self.password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
#
# This function returns the temperature and humidity
#
def TempHun():
 d = dht.DHT11(Pin(0))
 d.measure()
 t = d.temperature()
 h = d.humidity()
 return t, h
#
# Send data to Thingspeak. This function sends the temperature and
# humidity data to the cloud every 60 seconds
#
while True:
 Connect_WiFi()
 print ('connecet to wifi')
 sock = socket.socket()
 print (sock)
 addr = socket.getaddrinfo('api.thingspeak.com',80)[0][-1]
 print (addr)
 sock.connect(addr)
 print(sock.connect)
 (t, h) = TempHun()
 print (t , h)
 host = 'api.thingspeak.com'
 path = 'api_key='+APIKEY+'&field1='+ str(t)+'&field2='+ str(h)
 print (path)
 sock.send(bytes('GET /update?%s HTTP/1.0\r\nHost: %s\r\n\r\n'%(path,host),'utf8'))
 print (sock.send)
 sock.close()
 print ('sock.closed')
 time.sleep(10)


