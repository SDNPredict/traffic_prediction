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
parser.add_argument("-t", "--type", default=1, help="select 1 for select tcpreplay, 2 for dsp waves (default 2)")

args = parser.parse_args()
type = args.type

class TestTopology(Topo):

    def build(self):
        # Add the central switch
        s1 = self.addSwitch('s1')

        # connect n hosts to the switch
        hosts = []
        for h in range(0, 4):
            hosts.append(self.addHost("h{}".format(h+1), mac='00:00:00:00:00:0{}'.format(h+1)))
            self.addLink(s1, hosts[h], cls=TCLink, bw=40, delay='15ms')


class CustomTopology(Topo):

    def build(self):
        # Add the central switch
        s1 = self.addSwitch('s1')

        # connect n hosts to the switch
        hosts = []
        for h in range(0, 5):
            hosts.append(self.addHost("h{}".format(h+1)))
            self.addLink(s1, hosts[h], cls=TCLink, bw=40, delay='15ms')

        # Add the second switch
        s2 = self.addSwitch('s2')

        # connect n hosts to the switch
        for h in range(5, 10):
            hosts.append(self.addHost("h{}".format(h+1)))
            self.addLink(s2, hosts[h], cls=TCLink, bw=40, delay='15ms')

        # connect the switches
        self.addLink(s1, s2, cls=TCLink, bw=40, delay='15ms')


topos = {
    'Test': (lambda: TestTopology()),
    'Custom': (lambda: CustomTopology())
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
        topo=TestTopology(),
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
        #if type == 1:
        #    CLI(net, script='./pcap_traffic.sh')
        #elif type == 2:
        CLI(net, script='./dsp_traffic.sh')
        
        print(type)

        # For debug
        CLI(net)

    # Stop
    net.stop()

    # Clear
    system("sudo mn -c && clear")

if __name__ == "__main__":
    setLogLevel( 'info' )
    start() # For debug
