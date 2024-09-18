""" Server class and send function for transfer between application instances. """
import socket
import os
from PyQt5 import QtCore
import time

default_port = 51283


class DGramServer(QtCore.QObject):
    onFinish = QtCore.pyqtSignal(str)
    onRead = QtCore.pyqtSignal(str)

    def __init__(self, thread, port=default_port):
        super().__init__()
        self.thread = thread
        self.ipport = ('localhost', port)
        self.keep_running = False
        self.sock = None

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.sock.bind(self.ipport)
        except socket.error:
            print('can not open port',self.ipport)
            self.onFinish.emit('Ошибка открытия порта, возможно он уже занят')
            self.thread.quit()
            self.thread = None
            return
        except Exception as e:
            print('error', e)
            self.onFinish.emit(f'Ошибка: {str(e)}')
            self.thread.quit()
            self.thread = None
            return
        self.keep_running = True

        while self.keep_running:
            data = self.sock.recvfrom(65536)
            if len(data) > 0:
                self.onRead.emit(data[0].decode('utf-8'))
            else:
                time.sleep(0.1)
        self.sock.close()
        self.onFinish.emit(self)
        self.thread.quit()
        self.thread = None


def send(data, ip_port=('localhost', default_port)):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(data.encode('utf-8'), ip_port)
    except socket.error:
        print('sender error connection')
        return False
    except Exception as e:
        print('Sender exception: %s' % e)
        return False
    else:
        return True

