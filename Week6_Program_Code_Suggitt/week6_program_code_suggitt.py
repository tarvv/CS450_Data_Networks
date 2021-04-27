#!/usr/bin/env python
"""Creates a hexadecimal output string by concatenating an input and a calculated CRC32.

Input comes from either a file defined in the terminal argument or queries stdin. Next calculates a crc32 checksum.
Currently prints a hexadecimal string that is the concatenation of in data stream and checksum. The beginning function
returns this string. Given command flags, prints results of up to 3 different crc32 implementations, all of which have
the same results.
Created by Travis Suggitt for course CS450 Data Networks at Regis University
Date: 2-23-2021
"""

import sys
import argparse
import binascii
import zlib

BITS_IN_BYTE = 8
HEX_IN_128_BYTES = 256
BUFFER_SIZE_BYTES = 128

def get_built_crc32(data, val=0):
	"""Computes the same CRC-32 checksum of data as zlib.crc32(data, val).

	This is my Python implementation of the CRC32 algorithm without tables. Generator (polynomial) value is 0xedb88320
	as written in CRC wikipedia article (https://en.wikipedia.org/wiki/Cyclic_redundancy_check). The code is essentially
	a python translation from C versions that can be found in various forms ar the following urls:
	http://www.sunshine2k.de/articles/coding/crc/understanding_crc.html#ch6
	https://create.stephan-brumme.com/crc32/#bitwise
	https://ideone.com/pWLVSo
	https://zlib.net/crc_v3.txt (not an exact C implementation, but was useful)

	:param data: bytes object of data used to create a checksum
	:param val: [default=0] integer crc32 checksum to start algorithm with
	:return: integer crc32 checksum
	"""
	generator = 0xEDB88320
	val = ~val & 0xffffffff

	for i in range(len(data)):
		val ^= data[i]
		for k in range(BITS_IN_BYTE):
			if val & 1:
				val = (val >> 1) ^ generator
			else:
				val = val >> 1
	return ~val & 0xffffffff

def get_zlib_crc32(data, val=0):
	"""Helper function that returns zlib.crc32() with & 0xffffffff bitmask.

	:param data: bytes object of data used to create a checksum
	:param val: [default=0] integer crc32 checksum to start algorithm with
	:return: integer crc32 checksum
	"""
	return zlib.crc32(data, val) & 0xffffffff

def get_binascii_crc32(data, val=0):
	"""Helper function that returns binascii.crc32() with & 0xffffffff bitmask.

	:param data: bytes object of data used to create a checksum
	:param val: [default=0] integer crc32 checksum to start algorithm with
	:return: integer crc32 checksum
	"""
	return binascii.crc32(data, val) & 0xffffffff

def read_file_128(fname):
	"""Returns up to the first 128 bytes of a file

	:param fname: String name of file including path
	:return: bytes object with 128 bytes from file
	"""
	try:
		with open(fname, 'rb') as freader:
			return freader.read(BUFFER_SIZE_BYTES)
	except OSError as err:
		print(err)
		print('Shutting down...')
		sys.exit(1)
	except ValueError as err:
		print(err)
		print('Shutting down...')

def parser_setup():
	"""Sets up parser for command line arguments

	:return: Parser to be used for command line arguments
	"""
	parser = argparse.ArgumentParser(description='Create hex of 32 bit appended to 128 byte input')
	parser.add_argument('-Z', action='store_true', help='Use zlib.crc32()')
	parser.add_argument('-B', action='store_true', help='Use binascii.crc32()')
	parser.add_argument('-H', action='store_true', help='[DEFAULT] Use author\'s implementation')
	parser.add_argument('-A', action='store_true', help='Use all 3 implementations (zlib, binascii, and author)')
	parser.add_argument('filename', nargs='?', type=str, help='Name of file to use')
	return parser


def print_out_stream(data, crc, method):
	"""Prints the data input, crc32 checksum, and concatenation in human readable manner

	:param data: bytes object of data used to create a checksum
	:param crc: integer crc32 checksum
	:param method: String that defines what implementation is being printed
	"""
	data_hex = data.hex()
	crc_hex = hex(crc).lstrip('0x')
	msg_hex = data_hex + crc_hex
	print('{} CRC32 implementation'.format(method))
	print('Data hex:  ', data_hex)
	print('CRC32 hex: ', crc_hex)
	print('Output stream hex:')
	print(msg_hex)
	print()

def print_stream_handler(data, args):
	"""Handles argument flag logic to determine what should be printed

	:param data: bytes object of data used to create a checksum
	:param args: command line arguments formed by parse_args()
	"""
	crc = get_built_crc32(data)
	if args.A:
		print_out_stream(data, get_zlib_crc32(data), 'zLib')
		print_out_stream(data, get_binascii_crc32(data), 'binascii')
		print_out_stream(data, crc, 'Suggitt\'s')
	else:
		if args.Z:
			print_out_stream(data, get_zlib_crc32(data), 'zLib')
		if args.B:
			print_out_stream(data, get_binascii_crc32(data), 'binascii')
		if args.H or not args.Z and not args.B:
			print_out_stream(data, crc, 'Suggitt\'s')

def run_crc32():
	"""Runs the crc32 on an input and returns the input with crc32 appended as a hexadecimal string.

	First reads terminal arguments for input stream info and printing info. With a filename, the input stream is up to
	the first 128 bytes of the file. Without a filename, the input stream will be user stdin. Flags determine which
	implementation of CRC32 to print (function always returns the author's implementation).

	:return: hexadecimal string of input stream with crc32 checksum appended
	"""
	parser = parser_setup()
	args = parser.parse_args()
	if args.filename:
		data_bytes = read_file_128(args.filename)
		print('Using first 128 bytes of file \'{}\' for CRC32'.format(args.filename))
	else:
		try:
			data_bytes = input('Enter a line to use for CRC32: ').encode('ascii')
			if sys.getsizeof(data_bytes) <= sys.getsizeof(bytes()):
				print('No data entered. No calculations to make.')
				return
		except EOFError as err:
			print(err)
			print('Shutting down...')
			sys.exit(1)
		except ValueError as err:
			print(err)
			print('Shutting down...')
			sys.exit(1)

	print_stream_handler(data_bytes, args)
	return data_bytes.hex() + hex(get_built_crc32(data_bytes)).lstrip('0x')


run_crc32()
