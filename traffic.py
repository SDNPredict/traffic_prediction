from scapy.all import *
import scapy.contrib.openflow as of 
import sys
import math
import argparse

parser = argparse.ArgumentParser(description="Generate traffic through SDN")
parser.add_argument("dst", type=str, help="ip of destination")
parser.add_argument("-s", "--size", default=1000, help="packet size (default 1000)")
parser.add_argument("-p", "--period", default=2, help="period duration (default 2)")
parser.add_argument("-d", "--duration", default=10, help="duration of the program in seconds (default 10s)")

parser.add_argument(
args = parser.parse_args()

server_ip = args.dst
base_packet_size = int(args.size)
period = int(args.period)
duration = int(args.duration)

# def generate_traffic_size(delta): 
#     amplitude = 5
#     packet_size = base_packet_size + int(amplitude * math.sin(2 * math.pi * period * delta))
#     packet = IP(dst=server_ip)/ICMP()/Raw(load=b"*" * packet_size)
#     return packet

def generate_traffic(t):
    sin_value = abs(math.sin(2 * math.pi * t / period))
    if sin_value < 0.05:
        time.sleep(0.05)
        print("0.05")
    else:
        time.sleep(sin_value) 
        print(sin_value)

    packet = IP(dst=server_ip)/ICMP()
    # /Raw(load=b"*" * base_packet_size)
    return packet
 
counter = 0
start_time = time.time()
while time.time() - start_time < duration:
    current_time = time.time() - start_time
    #counter += 1
    send(generate_traffic(current_time))

