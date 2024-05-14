from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info

from os import system
from os.path import join
import json
import socket
import subprocess
import time
import argparse

parser = argparse.ArgumentParser(description="Generate traffic with tcp replay or with a traffic that emulate some dsp waves")
parser.add_argument("-t", "--wave_type", default=1, help="select 0 for tcpreplay, 1 for sine wave, 2 for triangular wave, 3 for sawtooth wave, 4 for square wave, 5 for mixed dsp waves (default 1)")

args = parser.parse_args()
wave_type = int(args.wave_type)

class Topology(Topo):

    def build(self):
        # Add the central switch
        s1 = self.addSwitch('s1')

        # connect n hosts to the switch
        hosts = []
        for h in range(0, 4):
            hosts.append(self.addHost("h{}".format(h+1), mac='00:00:00:00:00:0{}'.format(h+1)))
            self.addLink(s1, hosts[h], cls=TCLink, bw=40, delay='15ms')


class Enhanced(Topo):

    def build(self):
        hosts = []
        s1 = self.addSwitch('s1')
        for h in range(0, 3):
            hosts.append(self.addHost("h{}".format(h+1), mac='00:00:00:00:00:0{}'.format(h+1)))
            self.addLink(s1, hosts[h], cls=TCLink, bw=40, delay='15ms')

        s2 = self.addSwitch('s2')
        for h in range(3, 7):
            hosts.append(self.addHost("h{}".format(h+1), mac='00:00:00:00:00:0{}'.format(h+1)))
            self.addLink(s2, hosts[h], cls=TCLink, bw=40, delay='15ms')

        s3 = self.addSwitch('s3')
        for h in range(7, 10):
            hosts.append(self.addHost("h{}".format(h+1), mac='00:00:00:00:00:0{}'.format(h+1)))
            self.addLink(s3, hosts[h], cls=TCLink, bw=40, delay='15ms')


        self.addLink(s1, s2, cls=TCLink, bw=40, delay='15ms')
        self.addLink(s1, s3, cls=TCLink, bw=40, delay='15ms')
        self.addLink(s2, s3, cls=TCLink, bw=40, delay='15ms')         


topos = {
    'Main': (lambda: Topology()),
    'Enhanced': (lambda: Enhanced())
}


def start():

    global CURRENT_SCENARIO

    system("clear")
    
    system("ryu-manager controller.py &")

    # Create control if it's None
    controller = RemoteController("c1", "127.0.0.1", 6633)

    # Create Mininet object
    print("[INFO] Creating Mininet object")


    net = Mininet(
        topo=Topology(),
        switch=OVSKernelSwitch,
        controller=controller,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )

    # Build
    print("[INFO] Building")
    net.build()

    # Start
    print("[INFO] Starting")
    net.start()

    time.sleep(3)
    # The startup script for tcpdump should go here, so the network is instantiated 
    # and tcpdump can start listening and dumping the packets
    system("./tcpdump_script.sh")

    time.sleep(5)
    system("clear")

    if __name__ == "__main__":
        if wave_type == 0:
            CLI(net, script='../traffic/pcap_traffic.sh')
        elif wave_type == 1:
            CLI(net, script='../traffic/sine_traffic.sh')
        elif wave_type == 2:
            CLI(net, script='../traffic/triangular_traffic.sh')
        elif wave_type == 3:
            CLI(net, script='../traffic/sawtooth_traffic.sh')
        elif wave_type == 4:
            CLI(net, script='../traffic/square_traffic.sh')
        elif wave_type == 5:       
            CLI(net, script='../traffic/dsp_traffic.sh')

        # For debug
        CLI(net)

    # Stop
    net.stop()

    # Clear
    system("sudo mn -c && clear")

if __name__ == "__main__":
    setLogLevel( 'info' )
    start() # For debug
