#!/usr/bin/env python
"""Runs MD5 algorithm (RFC 1321) on an input file or input string.

Input comes from either a file defined in the terminal argument or queries stdin. Calculates and prints the input's MD5
hash. Given command flags, prints results of hashlib.md5(), my implementation, or both MD5 implementations. These should
return the same value.
Created by Travis Suggitt for Week 7 assignment of CS450 Data Networks at Regis University.
Date: 2-28-2021
"""
import sys
import argparse
import hashlib

BLOCK_BITS = 512
BLOCK_BYTES = BLOCK_BITS//8
PREPAD_BITS = 448
PREPAD_BYTES = PREPAD_BITS//8
HEX_BYTES = 4

def get_hashlib_md5(data):
	"""Gives the MD5 hash as calculated by hashlib.md5

	:param data: bytes string to be calculated
	:return: MD5 hex string
	"""
	return hashlib.md5(data).hexdigest()

def rotate_left(x, n):
	"""Rotates the x to the left by n

	:param x: 4 byte data to rotate
	:param n: amount of rotation
	:return: 4 byte x rotated n to the left
	"""
	x &= 0xffffffff
	return (x << n) | (x >> (32 - n))

def words_as_array(block):
	"""Makes an array by splitting 64 bytes of data into 16 even-sized words

	:param block: 64 bytes to be split
	:return: 16 member array
	"""
	word_array = []
	for i in range(0, BLOCK_BYTES, HEX_BYTES):
		word_array.append(int.from_bytes(block[i:i + HEX_BYTES], byteorder='little'))
	return word_array

"""
The following 4 functions are auxillary functions as defined in RFC 1321.
"""
def auxF(x, y, z):
	return (x & y) | ((~x) & z)

def auxG(x, y, z):
	return (x & z) | (y & (~z))

def auxH(x, y, z):
	return x ^ y ^ z

def auxI(x, y, z):
	return y ^ (x | (~z))

"""
The following 4 functions perform 1 round of modification
"""
def modF(a, b, c, d, x, s, ac):
	a = a + auxF(b, c, d) + x + ac
	a = rotate_left(a, s)
	a += b & 0xffffffff
	return a

def modG(a, b, c, d, x, s, ac):
	a = a + auxG(b, c, d) + x + ac
	a = rotate_left(a, s)
	a += b & 0xffffffff
	return a

def modH(a, b, c, d, x, s, ac):
	a = a + auxH(b, c, d) + x + ac
	a = rotate_left(a, s)
	a += b & 0xffffffff
	return a

def modI(a, b, c, d, x, s, ac):
	a = a + auxI(b, c, d) + x + ac
	a = rotate_left(a, s)
	a += b & 0xffffffff
	return a

def process_block(block, a, b, c, d):
	"""Processes a 512 bit (64 byte) block for MD5 hash

	Rotate values, constants, and function calls are hardcoded. The values can be found in RFC 1321
	(https://tools.ietf.org/html/rfc1321).

	:param block: 64 byte hex string to be processed
	:param a: 4 byte string section of MD5
	:param b: 4 byte string section of MD5
	:param c: 4 byte string section of MD5
	:param d: 4 byte string section of MD5
	:return: a, b, c, d after processesing
	"""
	# Rotate value
	s11 = 7
	s12 = 12
	s13 = 17
	s14 = 22
	s21 = 5
	s22 = 9
	s23 = 14
	s24 = 20
	s31 = 4
	s32 = 11
	s33 = 16
	s34 = 23
	s41 = 6
	s42 = 10
	s43 = 15
	s44 = 21

	x = words_as_array(block)

	# Last argument in function call is hardcoded constant, see RFC 1321
	a = modF(a, b, c, d, x[0], s11, 0xd76aa478)
	d = modF(d, a, b, c, x[1], s12, 0xe8c7b756)
	c = modF(c, d, a, b, x[2], s13, 0x242070db)
	b = modF(b, c, d, a, x[3], s14, 0xc1bdceee)
	a = modF(a, b, c, d, x[4], s11, 0xf57c0faf)
	d = modF(d, a, b, c, x[5], s12, 0x4787c62a)
	c = modF(c, d, a, b, x[6], s13, 0xa8304613)
	b = modF(b, c, d, a, x[7], s14, 0xfd469501)
	a = modF(a, b, c, d, x[8], s11, 0x698098d8)
	d = modF(d, a, b, c, x[9], s12, 0x8b44f7af)
	c = modF(c, d, a, b, x[10], s13, 0xffff5bb1)
	b = modF(b, c, d, a, x[11], s14, 0x895cd7be)
	a = modF(a, b, c, d, x[12], s11, 0x6b901122)
	d = modF(d, a, b, c, x[13], s12, 0xfd987193)
	c = modF(c, d, a, b, x[14], s13, 0xa679438e)
	b = modF(b, c, d, a, x[15], s14, 0x49b40821)

	a = modG(a, b, c, d, x[1], s21, 0xf61e2562)
	d = modG(d, a, b, c, x[6], s22, 0xc040b340)
	c = modG(c, d, a, b, x[11], s23, 0x265e5a51)
	b = modG(b, c, d, a, x[0], s24, 0xe9b6c7aa)
	a = modG(a, b, c, d, x[5], s21, 0xd62f105d)
	d = modG(d, a, b, c, x[10], s22, 0x2441453)
	c = modG(c, d, a, b, x[15], s23, 0xd8a1e681)
	b = modG(b, c, d, a, x[4], s24, 0xe7d3fbc8)
	a = modG(a, b, c, d, x[9], s21, 0x21e1cde6)
	d = modG(d, a, b, c, x[14], s22, 0xc33707d6)
	c = modG(c, d, a, b, x[3], s23, 0xf4d50d87)
	b = modG(b, c, d, a, x[8], s24, 0x455a14ed)
	a = modG(a, b, c, d, x[13], s21, 0xa9e3e905)
	d = modG(d, a, b, c, x[2], s22, 0xfcefa3f8)
	c = modG(c, d, a, b, x[7], s23, 0x676f02d9)
	b = modG(b, c, d, a, x[12], s24, 0x8d2a4c8a)

	a = modH(a, b, c, d, x[5], s31, 0xfffa3942)
	d = modH(d, a, b, c, x[8], s32, 0x8771f681)
	c = modH(c, d, a, b, x[11], s33, 0x6d9d6122)
	b = modH(b, c, d, a, x[14], s34, 0xfde5380c)
	a = modH(a, b, c, d, x[1], s31, 0xa4beea44)
	d = modH(d, a, b, c, x[4], s32, 0x4bdecfa9)
	c = modH(c, d, a, b, x[7], s33, 0xf6bb4b60)
	b = modH(b, c, d, a, x[10], s34, 0xbebfbc70)
	a = modH(a, b, c, d, x[13], s31, 0x289b7ec6)
	d = modH(d, a, b, c, x[0], s32, 0xeaa127fa)
	c = modH(c, d, a, b, x[3], s33, 0xd4ef3085)
	b = modH(b, c, d, a, x[6], s34, 0x4881d05)
	a = modH(a, b, c, d, x[9], s31, 0xd9d4d039)
	d = modH(d, a, b, c, x[12], s32, 0xe6db99e5)
	c = modH(c, d, a, b, x[15], s33, 0x1fa27cf8)
	b = modH(b, c, d, a, x[2], s34, 0xc4ac5665)

	a = modI(a, b, c, d, x[0], s41, 0xf4292244)
	d = modI(d, a, b, c, x[7], s42, 0x432aff97)
	c = modI(c, d, a, b, x[14], s43, 0xab9423a7)
	b = modI(b, c, d, a, x[5], s44, 0xfc93a039)
	a = modI(a, b, c, d, x[12], s41, 0x655b59c3)
	d = modI(d, a, b, c, x[3], s42, 0x8f0ccc92)
	c = modI(c, d, a, b, x[10], s43, 0xffeff47d)
	b = modI(b, c, d, a, x[1], s44, 0x85845dd1)
	a = modI(a, b, c, d, x[8], s41, 0x6fa87e4f)
	d = modI(d, a, b, c, x[15], s42, 0xfe2ce6e0)
	c = modI(c, d, a, b, x[6], s43, 0xa3014314)
	b = modI(b, c, d, a, x[13], s44, 0x4e0811a1)
	a = modI(a, b, c, d, x[4], s41, 0xf7537e82)
	d = modI(d, a, b, c, x[11], s42, 0xbd3af235)
	c = modI(c, d, a, b, x[2], s43, 0x2ad7d2bb)
	b = modI(b, c, d, a, x[9], s44, 0xeb86d391)

	return a, b, c, d

def process_data(data):
	"""Perform MD5 on a byte string

	First appends 0's to input so that input length(bits) is 448 mod 512. Then appends 64 bit representation of original
	input length. Each 64 bit block is sequentially processed in process_block() and added together in 4 words. Finally,
	the words are appended and returned.
	Full MD5 algorithm can be found in RFC 1321 (https://tools.ietf.org/html/rfc1321).

	:param data: Byte string of data to create an MD5 hash of
	:return: MD5 hash of input
	"""
	# Initialized values for a,b,c,d
	a = 0x67452301
	b = 0xefcdab89
	c = 0x98badcfe
	d = 0x10325476

	init_len = (len(data) * 8).to_bytes(8, byteorder='little')
	data.append(0x80)
	while len(data) % BLOCK_BYTES != PREPAD_BYTES:
		data.append(0)
	data += init_len

	init_words = [a, b, c, d]
	for i in range(0, len(data), BLOCK_BYTES):
		process_words = process_block(data[i:i + BLOCK_BYTES], a, b, c, d)

		for j, val in enumerate(process_words):
			init_words[j] += val
			init_words[j] &= 0xffffffff

	md5_hash = ''
	for k, val in enumerate(init_words):
		md5_hash += val.to_bytes(HEX_BYTES, byteorder='little').hex()
	return md5_hash


def read_file(fname):
	"""Returns byte string of a file

	:param fname: String name of file including path
	:return: bytes object of file
	"""
	try:
		with open(fname, 'rb') as freader:
			return freader.read()
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
	parser = argparse.ArgumentParser(description='Create MD5 of input from file or command')
	parser.add_argument('-H', action='store_true', help='Use hashlib.md5()')
	parser.add_argument('-S', action='store_true', help='[DEFAULT] Use author\'s implementation')
	parser.add_argument('-A', action='store_true', help='Use both implementations (hashlib and author)')
	parser.add_argument('filename', nargs='?', type=str, help='Name of file to use')
	return parser

def run_md5():
	"""Runs the MD5 algorithm on file or terminal input

	Uses parser to determine where to get the data for MD5 hashing. Prints MD5 results. MD5 implementation chosen by
	terminal arguments held in parser.
	"""
	parser = parser_setup()
	args = parser.parse_args()
	if args.filename:
		data = bytearray(read_file(args.filename))
		print('Reading from file \'{}\' for MD5'.format(args.filename))
	else:
		try:
			data = bytearray(input('Enter a line to use for MD5: ').encode('ascii'))
		except EOFError as err:
			print(err)
			print('Shutting down...')
			sys.exit(1)
		except ValueError as err:
			print(err)
			print('Shutting down...')
			sys.exit(1)
	print()
	if args.H:
		print('MD5 processed by hashlib.md5()')
		print(get_hashlib_md5(data))
	elif args.A:
		print('MD5 processed by hashlib.md5()')
		print(get_hashlib_md5(data))
		print()
		print('MD5 processed by author\'s implementation')
		print(process_data(data))
	else:
		print('MD5 processed by author\'s implementation')
		print(process_data(data))

run_md5()
