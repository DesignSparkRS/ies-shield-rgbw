# Designer Systems DS-RGBW LED Lighting Shield Raspberry-PI Demonstrator
 
# Requires Raspberry-PI A or B board
 
# DS-RGBW.S [A0 & A1 jumpers ON] connected to I2C interface (GPIO pin 3 SDA, pin 5 SCL)
 
# RGBW.py	Date: 13/7/13	Version: 1.00 

# Run from LX terminal window using 'sudo python RGBW.py

# Fades WHITE up/down, outputs a number of RGB colours and then cycles through colour wheel

# Note: May require I2C setup procedure on R-PI

# Use CTRL+C to exit


# import modules needed for this application
import smbus
import time

# NOTE: THE ZERO IN THE COMMAND BELOW MAY NEED CHANGING TO A '1' DEPENDING ON THE RASPBERRY PI USED
bus = smbus.SMBus(0)

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

# Main program
while True:
  
# All off 
        bus.write_byte_data(address,2,0)
        bus.write_byte_data(address,3,0)
        bus.write_byte_data(address,4,0)
        bus.write_byte_data(address,5,0)

# Fade white LED from 0 to 99%   
	for data in range(0,99):    
		writeRegister(2,data)
                time.sleep(0.01)

# Fade white LED from 99 to -1 
	for data in range(99,-1,-1):    
		writeRegister(2,data)
                time.sleep(0.01)

# Sleep 2 second
        time.sleep(2)

# Send RGBW colour (Pink)      
        writeRGBWregisters(255,88,67)             

# Sleep 2 second
        time.sleep(2)

# Send RGBW colour (Green)
        writeRGBWregisters(48,187,80)      
 
# Sleep 2 seconds       
        time.sleep(2)

# Send RGBW colour (Orange)
        writeRGBWregisters(243,99,20)

# Sleep 2 second
        time.sleep(2)
        
# Send RGBW colour (Dark Purple)
        writeRGBWregisters(86,54,80)

# Sleep 2 seconds
        time.sleep(2)
       
# Set colour wheel to start colour   
        writeHSBregister(0,255,255)

# Rotate though complete colour wheel by changing HSB Hue value     
        for hue in range(0,255):
               writeRegister(6,hue)
               time.sleep(000.1)

# Sleep 2 seconds
        time.sleep(2)





















