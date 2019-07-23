import logging
import os
import socket
import re

from driver import RF_MotorControllers_Driver
logger = logging.getLogger()

class ResponseType():
    NO_RESPONSE = "NO_RESPONSE"

class Comm():
    def __init__(self, unix_socket_path, *args, **kwargs):
        self.unix_socket_path = unix_socket_path
        self.connection = None
        self.welcome_socket = None
        self.motor = RF_MotorControllers_Driver()

    def serve(self):
        try:
            if os.path.exists(self.unix_socket_path):
                logger.warning('Unix socket {} already exist'.format(self.unix_socket_path))
                os.unlink(self.unix_socket_path)

            if self.welcome_socket != None:
                logger.warning('Welcome socket already istantiated')

            self.welcome_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.welcome_socket.bind(self.unix_socket_path)
            os.system('chown iocuser:ioc {}'.format(self.unix_socket_path))

            logger.info('Unix socket created at {}'.format(self.unix_socket_path))
            self.welcome_socket.listen(1)

            while True:
                logger.info('Unix welcome socket listening')
                connection, client_address = self.welcome_socket.accept()
                logger.info('Client {} connected'.format(client_address))

                connection.settimeout(30)

                self.handle_connection(connection)
        except:
            logger.exception('Comm exception')
        finally:
            self.welcome_socket.close()
            os.remove(self.unix_socket_path)
            logger.info('Comm server shutdown')
            self.welcome_socket = None

    def handle_connection(self, connection):
        try:
            while True:
                command = connection.recv(1024).decode('utf-8')
                response = ResponseType.NO_RESPONSE

                if command == 'DATA?':
                    response = 'DATA ' + self.motor.data()
                elif command == 'DRV_STS?':
                    response = self.motor.drvSts()
                else :
                    try:
                        match = re.search(r'DRV_ENBL (0|1)$', command)
                        if hasattr(match, 'group'):
                            response = self.motor.drvEnbl(int(match.group(1)))
                    except:
                        logger.exception('Wrong command')

                connection.sendall('{}\r\n'.format(response).encode('utf-8'))
                logger.debug('Command {} Length {}'.format(command, response))
        except:
            logger.exception('Connection exception')
        finally:
            logger.warning('Connection closed')
            connection.close()
