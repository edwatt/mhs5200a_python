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


#freq_sweep(10,100,1,0.1,freq_mag=3,waveform=1)
wrapper(':s1f0000200000')
wrapper(':s1w0')