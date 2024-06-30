import configparser
import logging
import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import TLS_FTPHandler, ThrottledDTPHandler
from pyftpdlib.servers import ThreadedFTPServer
import sys

config = configparser.ConfigParser()
config.read('config.conf')

USERNAME=config['credentials']['username']
PASSWORD=config['credentials']['password']
IP_ADDRESS=config['network']['ip_address']
PORT=int(config['network']['port'])
READ_LIMIT=int(config['settings']['read_limit'])
WRITE_LIMIT=int(config['settings']['write_limit'])
MAX_CONNECTIONS=int(config['settings']['max_connections'])
MAX_CONNECTIONS_PER_IP=int(config['settings']['max_connections_per_ip'])
CERTIFICATE=config['security']['certificate']
KEY=config['security']['private_key']
BANNER=config['settings']['banner']
DIRECTORY=config['directory']['folder']


class MyHandler(TLS_FTPHandler):
    def on_connect(self):
        logging.info(f"{self.remote_ip} connected")

    def on_disconnect(self):
        logging.info(f"{self.remote_ip} disconnected")

    def on_login(self, username):
        logging.info(f"{username} has logged in")

    def on_logout(self, username):
        logging.info(f"{username} has logged out")

    def on_file_sent(self, file):
        logging.info(f"Sent {file}")

    def on_file_received(self, file):
        logging.info(f"Received {file}")

    def on_incomplete_file_sent(self, file):
        logging.warning(f"Incomplete file sent {file}")

    def on_incomplete_file_received(self, file):
        logging.warning(f"Incomplete file received {file}")
        os.remove(file)
        logging.debug(f"Removed incomplete file {file}")


def main():
    authorizer = DummyAuthorizer()
    authorizer.add_user(USERNAME, PASSWORD, DIRECTORY, perm='elradfmwMT')
    authorizer.add_anonymous(os.getcwd())

    handler = MyHandler
    handler.authorizer = authorizer
    handler.certfile = CERTIFICATE
    handler.keyfile = KEY
    handler.banner = BANNER

    server = ThreadedFTPServer((IP_ADDRESS, PORT), handler)

    server.max_cons = MAX_CONNECTIONS
    server.max_cons_per_ip = MAX_CONNECTIONS_PER_IP

    dtp_handler = ThrottledDTPHandler
    dtp_handler.read_limit = READ_LIMIT
    dtp_handler.write_limit = WRITE_LIMIT

    handler.dtp_handler = dtp_handler

    logging.basicConfig(filename='myFTPs.log', level=logging.INFO)
    
    try:
        server.serve_forever()

    except KeyboardInterrupt:
        logging.info("Shutting down server")
        server.close_all()
        logging.info("Server stopped")
        sys.exit(0)


if __name__ == '__main__':
    main()