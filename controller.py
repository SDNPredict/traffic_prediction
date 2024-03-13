from ryu.controller import ofp_event
from ryu.controller.handler import set_ev_cls
from ryu.base import app_manager
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types

class Controller(app_manager.RyuApp):

    # Specifies the supported OpenFlow version. In this case only 1.3
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)

        # dictionary to store the MAC address of the hosts connected to each switch 
        # TODO: select topology and implement the mac_to_port dictionary
        self.mac_to_port = {}


    # define switch features handler 
    # called when the Ryu controller receives a EventOFPSwitchFeatures event from the switch
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # match all packets
        match = parser.OFPMatch()

        # send all packets to controller
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    # define add flow method
    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it to the switch
        mod = parser.OFPFlowMod(
            datapath=datapath, 
            priority=priority, 
            match=match, 
            instructions= [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        )

        # send the message to the switch
        datapath.send_msg(mod)

    # send packet to a switch and specify the output port
    def send_packet(self, msg, datapath, in_port, actions):
        # msg: message to be sent 
        # datapath: switch to send the message to
        # in_port: port where the message is received
        # actions: list of actions to be performed on the message if flow entry is matched

        data = None
        # if message has no buffer id, then assign the data to the message
        if msg.buffer_id == datapath.ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data
        )

        # send the message to the switch
        datapath.send_msg(out)
            

    # function called when the Ryu controller receives a EventOFPPacketIn event from the switch
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        # ev: event received from the switch (EventOFPPacketIn event)

        msg = ev.msg # message received from the switch
        datapath = msg.datapath # switch that sent the message
        ofproto = datapath.ofproto # OpenFlow protocol used by the switch
        parser = datapath.ofproto_parser # OpenFlow protocol parser used by the switch
        in_port = msg.match['in_port'] # port where the message is received

        # parse the packet
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        # if the packet is an LLDP packet
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return

        dst = eth.dst # destination MAC address of the packet
        dpid = datapath.id # datapath id of the switch

        # check if dst is inside the dpid map of the mac_to_port dictionary
        if dst in self.mac_to_port[dpid]:
            # output port is the port where the destination MAC address is connected
            out_port = self.mac_to_port[dpid][dst]
            # list of actions to be performed on the packet if flow entry is matched
            actions = [parser.OFPActionOutput(out_port)]

            # construct the match 
            match = parser.OFPMatch(eth_dst=dst)

            # add flow entry to the switch 
            self.add_flow(datapath, 1, match, actions)

            # send the packet to the output out_port 
            self.send_packet(msg, datapath, in_port, actions)
