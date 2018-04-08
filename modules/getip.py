import socket
import urllib.request


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    internal_ip = s.getsockname()[0]
    s.close()
    external_ip = urllib.request.urlopen('http://ident.me').read().decode('utf8')

    return internal_ip, external_ip
