import serial
import time
import math

def wrapper(command):
	ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1, rtscts=1)
	command = command +'\r\n'
	ser.write(command.encode())
	s = ser.read(100)
	print(s)

	ser.close()

def freq_sweep(start, stop, increment, hold_time, channel=1, freq_mag=1, waveform=None):

	ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=None, rtscts=1)

	if waveform:
		command = ':s' + str(channel) + 'w' + str(waveform) +'\r\n'
		print(command.strip(), end=" - ")
		ser.write(command.encode())
		resp = ser.readline()
		print(str(resp).strip())


	while 1:
		curr_f = start

		while curr_f <= stop:
			command = ':s' + str(channel) +'f' + freq_parse(curr_f, freq_mag) + '\r\n'
			print(command.strip(), end=" - ")
			ser.write(command.encode())
			resp = ser.readline()
			print(str(resp).strip())
			time.sleep(hold_time)
			curr_f = curr_f + increment


def freq_parse(freq,freq_mag=1):
	freq_hz = freq * math.pow(10,freq_mag)

	if freq_hz > 25000000 or freq_hz < 0:
		raise Exception

	freq_str = str(int(freq_hz))

	while(len(freq_str)) < 8:
		freq_str = '0' + freq_str

	freq_str = freq_str + '00'

	return freq_str

def generate_test_waveform():
	arb_w =[]

	i=0

	while i < 350:
		arb_w.append(255)
		i = i + 1

	while i < 700:
		arb_w.append(0)
		i = i + 1

	while i < 1024:
		arb_w.append(255)
		i = i + 1

	return arb_w

def generate_AM_waveform(carrier_freq, mod_freq, mod_factor):
	relative_freq = carrier_freq / mod_freq
	if relative_freq > 516:
		raise Exception

	arb_w = []

	for t in range(0,1024):
		value = ((1 + mod_factor*math.cos(2*math.pi*t/1024))*math.cos(2*math.pi*t*relative_freq/1024)/4 + 0.5)*255
		value = int(min(255,max(0,value)))
		arb_w.append(value)

	return arb_w

def arb_waveform():
	ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=None, rtscts=1)
	carrier_freq = 100000
	mod_freq = 15000

	arb_w = generate_AM_waveform(carrier_freq, mod_freq, 0.5)

	slice_num = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']

	for n in range(0,16):
		command = ':a0' + str(slice_num[n])
		for x in range(0,64):
			command = command + str(arb_w[n*64+x])
			if x != 63:
				command = command + ','
		command = command + '\r\n'
		print(command.strip(), end=" - ")
		ser.write(command.encode())
		resp = ser.readline()
		print(str(resp).strip())

	command = ':s1w100\r\n'
	print(command.strip(), end=" - ")
	ser.write(command.encode())
	resp = ser.readline()
	print(str(resp).strip())

	command = ':s1f' + freq_parse(mod_freq) + '\r\n'
	print(command.strip(), end=" - ")
	ser.write(command.encode())
	resp = ser.readline()
	print(str(resp).strip())




#freq_sweep(10,100,1,0.1,freq_mag=3,waveform=1)
#wrapper(':s1f0000200000')
#wrapper(':s1w0')

arb_waveform()