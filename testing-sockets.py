import imaplib
import pprint
import argparse
import socket
import ssl
import re
import os
import sys


# Create parser
parser = argparse.ArgumentParser(prog='imap_brute', description='IMAP bruting', add_help=False)

host_group = parser.add_mutually_exclusive_group(required=True)
host_group.add_argument('-h', help='host')
host_group.add_argument('-H', help='file with hosts')


user_group = parser.add_mutually_exclusive_group(required=True)
user_group.add_argument('-user', help='username')
user_group.add_argument('-U', help='file with usernames')

password_group = parser.add_mutually_exclusive_group(required=True)
password_group.add_argument('-pass', help='password')
password_group.add_argument('-P', help='file with passwords')

parser.add_argument('-tls', help='port', required=False, action='store_true')
parser.add_argument('-p', help='port', required=False)
parser.add_argument('--help', '-help', help='help menu', required=False, action='store_true')
parser.add_argument('-v', help='version', required=False, action='store_true')
parser.add_argument('-V', help='verbose', required=False, action='store_true')

args = vars(parser.parse_args())

def get_file(args):
	filename = args['P']
	if not os.path.exists(filename):
		print('The file does not exist: {}'.format(filename))
		
		sys.exit()
	else:
		data = [line.rstrip('\n') for line in open(filename)]
		return data
		

def host_connect(args):
	if args['tls']:
		if args['p']:
			imaplib.IMAP4_PORT = args['p']
			
		imapObj = imaplib.IMAP4_SSL(args['h'])
	else:
		if args['p']:
			imaplib.IMAP4_PORT = args['p']
			
		imapObj = imaplib.IMAP4(args['h'])
	
	return imapObj
		

def list_boxes(conn):
	status, labels = conn.list()
	if status == 'OK':
		respone = []
		for label in labels:
			#print(label.decode())
			children, folder = label.decode().replace('"', '').replace('\\', '').replace(' Junk', '').replace(' Trash', '').split(' / ')
			has_match = re.match('\(HasNoChildren.*|\(Marked HasNoChildren.*', children)
			has_child = re.match('\(HasChildren.*', children)
			if has_match:
				children = ''
			if has_child:
				#conn.select(folder)
				children = '\n\tSub Folders Availble'
			respone.append((folder, children))		
	return sorted(respone)

if __name__ == '__main__':
	if args['H']:
		host_list = get_file(args)
	
	if args['P']:
		pass_list = get_file(args)
	
	if args['U']:
		user_list = get_file(args)
	
	if args['h']:
		conn = host_connect(args)
		
		conn.login(args['user'], args['pass'])
		
		response = list_boxes(conn)
		print('Connected....listing folders\n')
		for folder, children in response:
			print(folder, children)
	
	
	

