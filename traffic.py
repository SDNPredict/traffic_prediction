from scapy.all import *
import scapy.contrib.openflow as of 
import sys
import math
import argparse

parser = argparse.ArgumentParser(description="Generate traffic through SDN")
parser.add_argument("dst", type=str, help="ip of destination")
parser.add_argument("-s", "--size", default=1000, help="packet size (default 1000)")
parser.add_argument("-f", "--freq", default=2, help="packet frequency (default 2)")
parser.add_argument("-d", "--duration", default=10, help="duration of the program in seconds (default 10s)")
args = parser.parse_args()

server_ip = args.dst
base_packet_size = int(args.size)
frequency = int(args.freq)
duration = int(args.duration)

def generate_traffic_size(delta): 
    amplitude = 5

    packet_size = base_packet_size + int(amplitude * math.sin(2 * math.pi * frequency * delta))

    packet = IP(dst=server_ip)/ICMP()/Raw(load=b"*" * packet_size)
    return packet


def generate_traffic(t):
    sin_value = abs(math.sin(frequency * t))

    time.sleep(sin_value)
    print(sin_value)

    packet = IP(dst=server_ip)/of.TCP()
    # /Raw(load=b"*" * base_packet_size)
    return packet
 
counter = 0
start_time = time.time()
while time.time() - start_time < duration:
    counter += 1
    send(generate_traffic(counter))

