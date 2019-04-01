import imaplib
import pprint
import argparse

imap_host = 'imap.gmail.com'
imap_user = 'darryllane101@gmail.com'
imap_pass = ''


# Create parser and suppress help to utilise our own
parser = argparse.ArgumentParser(prog='imap_brute', description='IMAP bruting', add_help=False)

parser.add_argument('-h', help='host', required=False)
parser.add_argument('-H', help='file with hosts', required=False)
parser.add_argument('-p', help='port', required=False)

parser.add_argument('-user', help='username', required=False)
parser.add_argument('-U', help='file with usernames', required=False)
parser.add_argument('-pass', help='password', required=False)
parser.add_argument('-P', help='file with passwords', required=False)

parser.add_argument('--help', '-help', help='help menu', required=False, action='store_true')
parser.add_argument('-v', help='version', required=False, action='store_true')
parser.add_argument('-V', help='verbose', required=False, action='store_true')

args = vars(parser.parse_args())

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(sock=sock, ssl_version=ssl.PROTOCOL_TLSv1)
ssl_sock.connect((args['h'], 993))
print()
