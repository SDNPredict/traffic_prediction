from mininet.topo import Topo
from mininet.link import TCLink

class TestTopology(Topo):

    def build(self):
        # Add the central switch
        s1 = self.addSwitch('s1')

        # connect n hosts to the switch
        hosts = []
        for h in range(0, 5):
            hosts.append(self.addHost("h{}".format(h+1)))
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
