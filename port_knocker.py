"""
Usage : python port_knocker.py

Author : Anonymous
"""

# CONSTANTS
PORT_RANDOM = 20000
PORT_MINIMUM = 1025
SYN_FLAG = "S"
SCAPY_RUNTIME = "scapy.runtime"

# IMPORTS
from scapy.all import *
import logging
import random
import network_interfaces

# LOGGING
logging.getLogger(SCAPY_RUNTIME).setLevel(logging.ERROR)


def main():
    """
        Purpose : knock those ports..
        :return:
    """

    knock_ports()


def knock_ports():
    """
        Purpose : knock chosen ports that are get as input.
    :return none:
    """
    s_iface = network_interfaces.get_requested_interface()
    d_ip = raw_input("please enter destination ip : ")
    d_port_list = _get_port_list()
    for d_port in d_port_list:
        s_port = _get_random_unused_port()
        tcp_packet = IP(dst=d_ip) / TCP(dport=d_port, sport=s_port, flags=SYN_FLAG)
        send(tcp_packet, iface=s_iface)


def _get_port_list():
    """
        does not handle exceptions...
    :return:
    """
    num_ports = int(raw_input("please enter num of destination ports : "))
    d_port_list = []
    for idx in range(num_ports):
        d_port_list.append(int(raw_input("enter port number %d : " % (idx + 1))))
    return d_port_list


def _get_random_unused_port():
    """
        Purpose: get a random port that is 99% sure not taken
        :return int: the port.
    """

    return int(random.random() * PORT_RANDOM) + PORT_MINIMUM


if __name__ == '__main__':
    main()
