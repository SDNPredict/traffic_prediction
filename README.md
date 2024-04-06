# Traffic Prediction in SDN networks
This project explores the application of machine learning for traffic prediction in Software-Defined Networking (SDN) environments. It leverages the following technologies:

    Mininet: A Python library for emulating network topologies, enabling the creation and experimentation with virtual networks.
    Ryu: A popular open-source SDN controller framework, providing the foundation for constructing your custom traffic management and data collection logic.
    Prophet by Meta: A well-established Facebook (now Meta) open-source library for time series forecasting, ideal for predicting future network traffic patterns.

### Project Objectives:

Design and implement an SDN network using Mininet, mimicking a real-world or custom topology.
Develop a Ryu application to:
Manage the network communication between hosts and switches.
Gather network traffic data for analysis and prediction.
Utilize Prophet to:
Preprocess and format the collected traffic data into a suitable format for machine learning.
Train and evaluate a Prophet forecasting model to predict future network traffic patterns.

### Potential Applications:

Network Capacity Planning: Proactive scaling and resource allocation to accommodate anticipated traffic fluctuations.
Quality of Service (QoS) Optimization: Prioritization of critical traffic flows based on predicted demands.
Anomaly Detection: Identification of unusual traffic patterns that may indicate potential security threats or network congestion.

### Getting Started:

Prerequisites: Ensure you have Python and the required libraries (Mininet, Ryu, Prophet) installed on your system. Refer to their respective documentation for installation instructions.
Clone the Repository: Use Git to clone this repository to your local machine.
Run the Experiment: Follow the instructions provided within the code (or create a dedicated README.md file for the experiment with specific steps) to execute the Mininet network, Ryu application, and Prophet model.

## Project Phases

### Creation of the topology

### Generation of the network traffic

### Packet Acquisition

In order to gain detailed insight into individual host communication, we opted to use tcpdump, a network troubleshooting and packet capture utility. To achieve this, we specified the network interface associated with each host, ensuring we intercepted the relevant network traffic.  
This tool is useful for our purpose because with the flag `-w`, alongside a file name, it generates a pcap file, convenient to be read with software such as wireshark and in this way have a first sight of the traffic.  
  
With the command seen before (`sudo python3 topology.py`), not only the traffic starts to be sended, but also the script `tcpdump_script.sh` execute tcpdump (with the `&` to run the tool in background alongside mininet) and after the simulation, four pcap files are saved into the pc, one for each network interface.  

    File: tcpdump_script.sh
   
    1   │ #!/bin/bash
    2   │ 
    3   │ HOSTS=4
    4   │ 
    5   │ for ((i = 1; i <= $HOSTS; i++)); do
    6   │   echo "starting host_$i"
    7   │   sudo tcpdump -i s1-eth${i} -w ./dumps/h${i}_traffic.pcap -U &
    8   │ done
    9   │ 

 
Then, we have read the content of the pcap files with Wireshark and saved using the option `File > Export Packet Dissections > As CSV`.  
We found useful use Wireshark because it allowed us to have a fast sight of the traffic on the various interfaces, even though we have could used python libraries such as `dpkt` to convert `.pcap` files into `.csv`.  
After this passage, when these csv files have been generated, using Python we selected only the first and the second column of the csvs, the ones where are located the numbers of the packets, and their timestamps, and resaved as CSV, in such a way that these files could be read by Prohpet.    

### Data Elaboration

### Analysis of the Capture files

### Prediction with Prophet

### Observations and notes


