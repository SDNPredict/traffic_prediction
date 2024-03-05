from scapy.all import *
import sys
import math
import argparse

parser = argparse.ArgumentParser(description="Generate traffic through SDN")
parser.add_argument("dst", type=str, help="ip of destination")
parser.add_argument("size", type=str, help="packet size")
parser.add_argument("freq", type=str, help="packet frequency")
parser.add_argument("duration", type=str, help="duration of the program")
args = parser.parse_args()

server_ip = args.dst
base_packet_size = int(args.size)
frequency = int(args.freq)
duration = int(args.duration)

def generate_traffic(delta): 
    amplitude = 500

    packet_size = base_packet_size + int(amplitude * math.sin(2 * math.pi * frequency * delta))

    packet = IP(dst=server_ip)/ICMP()/Raw(load=b"*" * packet_size)
    return packet


start_time = time.time()
while time.time() - start_time < duration:
    send(generate_traffic(time.time() - start_time))
    time.sleep(1 / frequency)

