import socket
import struct
import fcntl

__author__ = 'scotm'

from . import base

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

DEBUG = False

ADMINS += (
    ('Scott Macdonald', 'scott.scotm@gmail.com'),
)

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [get_ip_address('eth0'), 'membership.scottishsocialistparty.org']

