from scapy.all import *
import scapy.contrib.openflow as of
import sys
import math
import argparse

parser = argparse.ArgumentParser(description="Generate traffic through SDN")
parser.add_argument("dst", type=str, help="ip of destination")
parser.add_argument("-w", "--wave", type=str, help="type of wave to generate (available options: sine, triangular, sawtooth, square")
parser.add_argument("-p", "--period", default=2, help="period duration (default 2)")
parser.add_argument("-d", "--duration", default=10, help="duration of the program in seconds (default 10s)")

args = parser.parse_args()
server_ip = args.dst
period = int(args.period)
duration = int(args.duration)
wave = args.wave


def generate_traffic(t):
    sin_value = abs(math.sin(2 * math.pi * t / period))
    if sin_value < 0.05:
        time.sleep(0.05)
        print("0.05")
    else:
        time.sleep(sin_value)
        print(sin_value)

    packet = IP(dst=server_ip) / ICMP()
    return packet

def generate_triangular_traffic(t):
    """
    This function generates a triangular wave with the given time (t)
    """
    amplitude = 1
    if t < 0:
        raise ValueError("t must be positive")

    triangular_value = abs((4 * amplitude / period) * abs(((t - (period / 4)) % period) - (period / 2)) - amplitude)

    if triangular_value < 0.05:
        time.sleep(0.05)
        print("0.05")
    else:
        time.sleep(triangular_value)
        print(triangular_value)

    packet = IP(dst=server_ip) / ICMP()
    return packet

def generate_sawtooth_traffic(t):
    """
    This function generates a sawtooth wave with the given time (t)
    """
    amplitude = 1
    if t < 0:
        raise ValueError("Time (t) must be positive")

    sawtooth_value = 2*((t/period)-math.floor((t/period)+0.5))

    if sawtooth_value < 0:
        sawtooth_value = 1 + sawtooth_value

    if sawtooth_value < 0.025:
        time.sleep(0.025)
        print(sawtooth_value)
    else:
        time.sleep(sawtooth_value)
        print(sawtooth_value)

    packet = IP(dst=server_ip) / ICMP()
    return packet

def generate_square_traffic(t):
    """
    This function generates a square wave with the given time (t)
    """
    amplitude = 0.5
    if t < 0:
        raise ValueError("Time (t) must be positive")

    #square_value = 4*math.floor(t)-2*math.floor(2*t)+1
    
    square_value = amplitude if (t % period) < (period / 2) else 0

    if square_value < 0.05:
        time.sleep(1)
    else:
        time.sleep(square_value)
        print(square_value)
        packet = IP(dst=server_ip) / ICMP()
        return packet

if __name__ == "__main__":
    counter = 0
    start_time = time.time()
    while time.time() - start_time < duration:
        current_time = time.time() - start_time
        if wave == "sine":
            send(generate_traffic(current_time))
        elif wave == "triangular":
            send(generate_triangular_traffic(current_time))
        elif wave == "sawtooth":
            send(generate_sawtooth_traffic(current_time))
        elif wave == "square":
            packet = generate_square_traffic(current_time)
            if packet is not None:
                send(packet)

