
import Adafruit_BBIO.GPIO as GPIO
import spicon
import time

DAC_pin = "P9_23"
ADC_pin = "P9_24"
ADC2_pin = "P9_26"

# SPI setup
# It is needed to have spidev overlay loaded!
spi = spicon.open("/dev/spidev0.0")
spicon.set_speed_mode(spi, 2000000, 1)


class DAC():
	def __init__(self):
		# Pin Setup
		GPIO.setup(DAC_pin, GPIO.OUT)
		GPIO.output(DAC_pin, GPIO.HIGH)

		# DAC Initial Setup
		GPIO.output(DAC_pin, GPIO.LOW)
		spicon.transfer(spi, '\x35\x96\x30')
		GPIO.output(DAC_pin, GPIO.HIGH)

		GPIO.output(DAC_pin, GPIO.LOW)
		spicon.transfer(spi, '\x20\x00\x00')
		#spicon.transfer(spi, '\x50\xFF\x80')
		#spicon.transfer(spi, '\x10\xFF\xF0')
		#spicon.transfer(spi, '\x33\x96\x30')
		GPIO.output(DAC_pin, GPIO.HIGH)


	def write(self, data = 0, channels = 0): # Write at DAC
		if type(channels) is list:
			if type(data) is list:
				for index, value in enumerate(channels):
					GPIO.output(DAC_pin, GPIO.LOW)
					spicon.transfer(spi, chr(0xB0+value)+chr(data[index]>>4)+chr((data[index]<<4)&0xff))
					GPIO.output(DAC_pin, GPIO.HIGH)

			else:
				for value in channels:
					GPIO.output(DAC_pin, GPIO.LOW)
					spicon.transfer(spi, chr(0xB0+value)+chr(data>>4)+chr((data<<4)&0xff))
					GPIO.output(DAC_pin, GPIO.HIGH)
		else:
			GPIO.output(DAC_pin, GPIO.LOW)
			spicon.transfer(spi, chr(0xB0+channels)+chr(data>>4)+chr((data<<4)&0xff))
			GPIO.output(DAC_pin, GPIO.HIGH)

	def WD_RESET(self):
		GPIO.output(DAC_pin, GPIO.LOW)
		spicon.transfer(spi, '\x33\x96\x30')
		GPIO.output(DAC_pin, GPIO.HIGH)
		return

	def SW_RESET(self):
		GPIO.output(DAC_pin, GPIO.LOW)
		spicon.transfer(spi, '\x35\x96\x30')
		GPIO.output(DAC_pin, GPIO.HIGH)
		return

class ADC():
	def __init__(self):
		# Pin Setup
		GPIO.setup(ADC_pin, GPIO.OUT)
		GPIO.output(ADC_pin, GPIO.HIGH)

		# ADC Initial Setup

		# Dummy Conversion - DIN line high
		GPIO.output(ADC_pin, GPIO.LOW)
		spicon.transfer(spi, '\xff\xff')
		GPIO.output(ADC_pin, GPIO.HIGH)

		# Dummy Conversion - DIN line high
		GPIO.output(ADC_pin, GPIO.LOW)
		spicon.transfer(spi, '\xff\xff')
		GPIO.output(ADC_pin, GPIO.HIGH)

		# Byte 1.1: | Write to Control Reg | Sequence = Continuous | DontCare | ADDR2 | 
                # Byte 1.0: | ADDR1 | ADDR0 | OpMode1 = Full power | OpMode0 = Full power
                # Byte 0.2: | Shadow = Continuous | DontCare | Range = 2xVref | Coding = Straight binary |
                # Byte 0.1: | DontCare | DontCare | DontCare | DontCare |
		GPIO.output(ADC_pin, GPIO.LOW)
		spicon.transfer(spi, '\x83\x10')
		GPIO.output(ADC_pin, GPIO.HIGH)


	def read(self, channels):

		if type(channels) is list:
			_channels = channels[:]
			_channels.append(channels[0])
			data = []
			# Initial command - Selection of first channel
			# ADC gives data from previous channel configuration
			GPIO.output(ADC_pin, GPIO.LOW)
			spicon.transfer(spi, chr(0x83 + channels[0]*4) + chr(0x10))
			GPIO.output(ADC_pin, GPIO.HIGH)

			for index in range (len(channels)):
				GPIO.output(ADC_pin, GPIO.LOW)
				_data = map(ord, spicon.transfer(spi, chr(0x83 + _channels[index+1]*4) + chr(0x10)))
				GPIO.output(ADC_pin, GPIO.HIGH)

				_data = (_data[0]&0x0F)*256 + _data[1]
				data.append(_data)

		else:
			GPIO.output(ADC_pin, GPIO.LOW)
			spicon.transfer(spi, chr(0x83 + channels*4) + chr(0x10))
			GPIO.output(ADC_pin, GPIO.HIGH)

			_data = map(ord, spicon.transfer(spi, chr(0x83 + channels*4) + chr(0x10)))
			data = (_data[0]&0x0F)*256 + _data[1]

		return data



class ADC2():
	def __init__(self):
		# Pin Setup
		GPIO.setup(ADC2_pin, GPIO.OUT)
		GPIO.output(ADC2_pin, GPIO.HIGH)

		# ADC Initial Setup

		# Dummy Conversion - DIN line high
		GPIO.output(ADC2_pin, GPIO.LOW)
		spicon.transfer(spi, '\xff\xff')
		GPIO.output(ADC2_pin, GPIO.HIGH)

		# Dummy Conversion - DIN line high
		GPIO.output(ADC2_pin, GPIO.LOW)
		spicon.transfer(spi, '\xff\xff')
		GPIO.output(ADC2_pin, GPIO.HIGH)

		# Byte 1.1: | Write to Control Reg | Sequence = Continuous | DontCare | ADDR2 | 
                # Byte 1.0: | ADDR1 | ADDR0 | OpMode1 = Full power | OpMode0 = Full power
                # Byte 0.2: | Shadow = Continuous | DontCare | Range = 2xVref | Coding = Straight binary |
                # Byte 0.1: | DontCare | DontCare | DontCare | DontCare |
		GPIO.output(ADC2_pin, GPIO.LOW)
		spicon.transfer(spi, '\x83\x10')
		GPIO.output(ADC2_pin, GPIO.HIGH)


	def read(self, channels):

		if type(channels) is list:
			_channels = channels[:]
			_channels.append(channels[0])
			data = []
			# Initial command - Selection of first channel
			# ADC gives data from previous channel configuration
			GPIO.output(ADC2_pin, GPIO.LOW)
			spicon.transfer(spi, chr(0x83 + channels[0]*4) + chr(0x10))
			GPIO.output(ADC2_pin, GPIO.HIGH)

			for index in range (len(channels)):
				GPIO.output(ADC2_pin, GPIO.LOW)
				_data = map(ord, spicon.transfer(spi, chr(0x83 + _channels[index+1]*4) + chr(0x10)))
				GPIO.output(ADC2_pin, GPIO.HIGH)

				_data = (_data[0]&0x0F)*256 + _data[1]
				data.append(_data)

		else:
			GPIO.output(ADC2_pin, GPIO.LOW)
			spicon.transfer(spi, chr(0x83 + channels*4) + chr(0x10))
			GPIO.output(ADC2_pin, GPIO.HIGH)

			_data = map(ord, spicon.transfer(spi, chr(0x83 + channels*4) + chr(0x10)))
			data = (_data[0]&0x0F)*256 + _data[1]

		return data
