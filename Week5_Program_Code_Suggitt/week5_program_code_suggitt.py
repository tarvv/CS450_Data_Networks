from socket import *
import os
import sys
import struct
import time
import select
import binascii
"""
week5_program_code_suggitt.py is an ICMP client program that will send an ICMP ping request to the provided address. The
program then watches for an ICMP reply and either prints the delay or a time out message.

Program completed as an assignment in CS450 Data Networks at Regis University. Bulk of program was provided by the class
textbook supplemental material (Kurose, J. F. & Ross, K. W. (2017). Computer networking: A top-down approach (7th 
edition). Pearson Education, Inc.). Student modified lines (aside from this header comment) are marked before and after
with single line block comments.

Modification Author: Travis Suggitt
Date: 2/14/2021
"""

ICMP_ECHO_REQUEST = 8

""" MODIFIED BY TRAVIS SUGGITT """
ICMP_ECHO_REPLY = 0
SEC_TO_MS = 1000
""" END OF MODIFIED LINES """

def checksum(string):
	csum = 0
	countTo = (len(string) // 2) * 2
	count = 0

	while count < countTo:
		thisVal = ord(string[count+1]) * 256 + ord(string[count])
		csum = csum + thisVal
		csum = csum & 0xffffffff
		count = count + 2

	if countTo < len(string):
		csum = csum + ord(string[len(string) - 1])
		csum = csum & 0xffffffff

	csum = (csum >> 16) + (csum & 0xffff)
	csum = csum + (csum >> 16)
	answer = ~csum
	answer = answer & 0xffff
	answer = answer >> 8 | (answer << 8 & 0xff00)
	return answer

def receiveOnePing(mySocket, ID, timeout, destAddr):
	timeLeft = timeout

	while 1:
		startedSelect = time.time()
		whatReady = select.select([mySocket], [], [], timeLeft)
		howLongInSelect = (time.time() - startedSelect)
		if whatReady[0] == []:  # Timeout
			return "Request timed out."

		timeReceived = time.time()
		recPacket, addr = mySocket.recvfrom(1024)
		#Fill in start
		#Fetch the ICMP header from the IP packet

		""" MODIFIED BY TRAVIS SUGGITT """
		header = recPacket[20:28]  # ICMP header is byte 20 to byte 28 of IP header
		icmpType, icmpCode, icmpChecksum, icmpId, icmpSeqNum = struct.unpack("bbHHh", header)
		if icmpId == ID and icmpCode == ICMP_ECHO_REPLY:
			timeRequested = struct.unpack("d", recPacket[28:28 + struct.calcsize("d")])[0]
			responseMs = (timeReceived - timeRequested) * SEC_TO_MS
			return "Response time: " + "{:.3f}".format(responseMs) + " ms"
		""" END OF MODIFIED LINES """

		#Fill in end
		timeLeft = timeLeft - howLongInSelect
		if timeLeft <= 0:
			return "Request timed out."

def sendOnePing(mySocket, destAddr, ID):
	# Header is type (8), code (8), checksum (16), id (16), sequence (16)

	myChecksum = 0

	# Make a dummy header with a 0 checksum
	# struct -- Interpret strings as packed binary data
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	data = struct.pack("d", time.time())
	# Calculate the checksum on the data and the dummy header.
	myChecksum = checksum(str(header + data))

	# Get the right checksum, and put in the header
	if sys.platform == 'darwin':
		# Convert 16-bit integers from host to network byte order
		myChecksum = htons(myChecksum) & 0xffff
	else:
		myChecksum = htons(myChecksum)

	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	packet = header + data

	mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str
	# Both LISTS and TUPLES consist of a number of objects
	# which can be referenced by their position number within the object.

def doOnePing(destAddr, timeout):
	icmp = getprotobyname("icmp")
	# SOCK_RAW is a powerful socket type. For more details: http://sock-raw.org/papers/sock_raw

	mySocket = socket(AF_INET, SOCK_RAW, icmp)

	myID = os.getpid() & 0xFFFF	 # Return the current process i
	sendOnePing(mySocket, destAddr, myID)
	delay = receiveOnePing(mySocket, myID, timeout, destAddr)
	mySocket.close()
	return delay

def ping(host, timeout=1):
	# timeout=1 means: If one second goes by without a reply from the server,
	# the client assumes that either the client's ping or the server's pong is lost
	dest = gethostbyname(host)
	print("Pinging " + dest + " using Python:")
	print("")
	# Send ping requests to a server separated by approximately one second
	while 1:
		delay = doOnePing(dest, timeout)
		print(delay)
		time.sleep(1)  # one second
	return delay

""" MODIFIED BY TRAVIS SUGGITT """
if len(sys.argv) == 2:
	try:
		ping(sys.argv[1])
	except KeyboardInterrupt:
		print("\nExit request received. Program shutting down.")
elif len(sys.argv) == 3:
	try:
		ping(sys.argv[1], int(sys.argv[2]))
	except ValueError:
		print("Incorrect argument type! Argument \"timeout seconds\" must be integer")
		print("Command format: \"week5_program_code_suggitt.py [destination] [optional: timeout seconds]\"")
	except KeyboardInterrupt:
		print("\nExit request received. Program shutting down.")
else:
	print("Incorrect number of arguments supplied! Program needs 1 or 2 arguments!")
	print("Command format: \"week5_program_code_suggitt.py [destination] [optional: timeout seconds]\"")
	exit()
""" END OF MODIFIED LINES """
