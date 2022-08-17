import machine
import sh1106
import dht
from umqttsimple import MQTTClient


class main():
    
    def __init__(self):
        #MQTT
        self.client_id = ubinascii.hexlify(machine.unique_id())
        self.mqtt_server = 'duckmqttduck.northeurope.cloudapp.azure.com'
        self.topic_sub = b'notification'
        self.topic_pub = b'b3_temp'
        self.topic2_pub = b'b3_humi'

        self.last_message = 0
        self.message_interval = 5
        
        #DHT11 Data Pin.
        self.d = dht.DHT11(machine.Pin(0)) #GPIO 0 (D3)

        #SPI Details.
        self.spi = machine.SPI(1, baudrate=1000000)

        #Oled Pin Settings.
        self.dc = machine.Pin(5) #GPIO 5 (D1)
        self.res = machine.Pin(4) #GPIO 4 (D2)
        self.cs = machine.Pin(15) #GPIO 15 (D8)

        #Oled Display Settings.
        self.oled_width = 128
        self.oled_height = 64
        
        #Display and Pin setting send to the sh1106 display driver using SPI for display output.
        self.oled = sh1106.SH1106_SPI(self.oled_width, self.oled_height, self.spi, self.dc, self.res, self.cs)
        
        #Starting MQTT connection - Restarts if connection is unsuccesfull.
        try:
            self.oled.fill(0)
            self.oled.text("Trying", 0, 16)
            self.oled.text("to", 0, 24)
            self.oled.text("connect", 0, 30)
            self.oled.show()
            self.client = self.connect_and_subscribe()
        except OSError as e:
            print('Failed to connect to MQTT broker. Reconnecting...')
            self.oled.fill(0)
            self.oled.text("Reconnecting", 0, 24)
            self.oled.show()
            self.restart_and_reconnect()


    def sens_data(self):
        #This Method pulls data from the sensor, while also checking with the Sensor is working.
        while True:
            try:
                self.d.measure()
                self.temp = self.d.temperature()
                self.humi = self.d.humidity()
                break
            except OSError as e:
                print("Check The Sensor")
                self.oled.fill(0)
                self.oled.text("Check", 0, 16)
                self.oled.text("The", 0, 24)
                self.oled.text("Sensor", 0, 30)
                self.oled.show()
                time.sleep(2)
                continue


    def clear_display(self):
        #This Method clears the display, by filling it with black.
        self.oled.fill(0)
        self.oled.show()
        

    def sub_cb(self,topic,msg):
        print((topic, msg))
        if topic == b'notification' and msg == b'received':
            print('ESP received hello message')

    def connect_and_subscribe(self):
        self.client = MQTTClient(self.client_id, self.mqtt_server)
        self.client.set_callback(self.sub_cb)
        self.client.connect()
        self.client.subscribe(self.topic_sub)
        print('Connected to %s MQTT broker, subscribed to %s topic' % (self.mqtt_server, self.topic_sub))
        return self.client

    def restart_and_reconnect(self):
        time.sleep(10)
        self.clear_display()
        machine.reset()
        
    def duck(self):
        print("           ..")
        print("          ( '`<")
        print("           )(")
        print("    ( ----'  '.")
        print("    (         ;")
        print("     (_______,'")
        print("~^~^~^~^~^~^~^~^~^~^~")
        self.oled.fill(0)
        self.oled.text("           ..", 0, 0)
        self.oled.text("          ( '`<", 0, 8)
        self.oled.text("           )(", 0, 16)
        self.oled.text("    ( ----'  '.", 0, 24)
        self.oled.text("    (         ;", 0, 30)
        self.oled.text("     (_______,'", 0, 38)
        self.oled.text("~^~^~^~^~^~^~^~^~^~^~", 0, 44)
        self.oled.show()
        time.sleep(5)
        
    def main_method(self):
        while True:
            try:
                self.client.check_msg()
                self.sens_data()
                print("Temperature:%iC" %(self.temp))
                print("Humidity:%i" %(self.humi))
                
                
                if (time.time() - self.last_message) > self.message_interval:
                    msg = b'%i' %self.temp
                    msg2 = b'%i' %self.humi
                    self.client.publish(self.topic_pub, msg, qos=1)
                    self.client.publish(self.topic2_pub, msg2, qos=1)
                    self.last_message = time.time()

                
                self.oled.fill(0)
                self.oled.text("Temperature:%iC" %(self.temp), 0, 16)
                self.oled.text("Humidity:%i" %(self.humi), 0, 24)
                self.oled.show()
            except OSError as e:
                print("Somthing went wrong.")
                self.oled.fill(0)
                self.oled.text("Somthing", 0, 16)
                self.oled.text("went", 0, 24)
                self.oled.text("wrong", 0, 30)
                self.oled.show()
                self.restart_and_reconnect()
            time.sleep(1)

        
if __name__ == "__main__":
    print("--Starting Machine--")
    ma = main()
    try:
        ma.duck()
        ma.main_method()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        ma.clear_display()
        print("--Stopping--")
