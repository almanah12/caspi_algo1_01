"""
Miscellaneous helper functions and constants.
"""

import os
import sys

from cryptography.fernet import Fernet
from loguru import logger
from http.server import HTTPServer, CGIHTTPRequestHandler
from pyngrok import ngrok

BASE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(BASE_DIR)

log_file_path = os.path.join(BASE_DIR, 'Logs/check.log')
logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
logger.add(log_file_path, rotation="00:00", retention="30 days", encoding='utf-8', level="INFO")


def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def get_current_version() -> str:
    """
    Reads version from version.txt and returns it.
    """
    version_file = resource_path(r'data_files/data_update_app/version.txt')

    if not os.path.isfile(version_file):
        version = 'not found'
    else:
        with open(version_file) as f:
            version = f.read().strip()

    return version


# Зашифруем файл и записываем его
def encrypt(filename, key):
    f = Fernet(key)
    with open(filename, 'rb') as file:
        # прочитать все данные файла
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)

    # записать зашифрованный файл
    with open(filename, 'wb') as file:
        file.write(encrypted_data)


# Расшифруем файл и записываем его
def decrypt(filename, key):
    f = Fernet(key)
    with open(filename, 'rb') as file:
        # читать зашифрованные данные
        encrypted_data = file.read()
    # расшифровать данные
    decrypted_data = f.decrypt(encrypted_data)
    # записать оригинальный файл
    with open(filename, 'wb') as file:
        file.write(decrypted_data)


public_url = ngrok.connect(8000).public_url
print("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, 8000))


def server_http_ngrok():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
    try:
        # Block until CTRL-C or some other terminating event
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(" Shutting down server.")

        httpd.socket.close()
