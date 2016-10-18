
# Copyright (c) <2016>, <AB Open>
#All rights reserved.

#Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

#1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

#2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

#3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.




#!/usr/bin/python

# Subscribe to MQTT topic and control IES RGBW LED shield/HAT/board

import os
import sys
import time
import json
import paho.mqtt.client as mqtt
import smbus

broker = "127.0.0.1"
topic = "RGBW-LED"

bus = smbus.SMBus(1)

# IES-RGBW

## Taken from demo RGBW.py

# Define DS-RGBW.S I2C address
address = 0x70

# Routine to write to I2c register from DS-RGBW.S
def writeRegister (register, value):
        bus.write_byte_data(address, register, value)

# Routine to write to I2c,define registers
def writeRGBWregisters (red, green, blue):
        bus.write_byte_data(address,3,red)
        bus.write_byte_data(address,4,green)
        bus.write_byte_data(address,5,blue)

# Routine to write to i2c, define registers
def writeHSBregister (hue,saturation,brightness):
        bus.write_byte_data(address,6,hue)
        bus.write_byte_data(address,7,saturation)
        bus.write_byte_data(address,8,brightness)

# MQTT
## The callback for when the client receives a CONNACK response from the server.

def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        print "Broker = " + broker + " Topic = " + topic
        client.subscribe(topic, 0)

## The callback for when a PUBLISH message is received from the server

def on_message(client, userdata, msg):
        print msg.payload
	disp = json.loads((msg.payload))

        try:
            if disp['command'] == 'RGB':

                print "Setting colour in RGB mode"
                writeRGBWregisters(disp['r'], disp['g'], disp['b'])

            elif disp['command'] == 'HSB':

                print "Setting colour in HSB mode"
                writeHSBregister(disp['hue'],disp['sat'],disp['bri'])

            elif disp['command'] == "WHI":

                print "Setting colour in White mode"
                writeRGBWregisters(0, 0, 0)
                writeRegister(2,disp['w'])

            elif disp['command'] == 'OFF':

                print "Turning LED off"
                writeRGBWregisters(0, 0, 0)
                writeHSBregister(0, 0, 0)

            else:
                print "Invalid command"
        except (KeyboardInterrupt, SystemExit):
            raise
        except (KeyError):
            print "Invalid command: key error"
        except:
            print "Undefined Error"

## Setup client

client = mqtt.Client("python_pub")
client.on_connect = on_connect
client.on_message = on_message

# Main loop

try:
    client.connect(broker, 1883, 60)
except (KeyboardInterrupt, SystemExit):
    raise
except:
    print "Failed to connect to broker"
    time.sleep(1)

## Run loop and wait for messages

client.loop_forever()
