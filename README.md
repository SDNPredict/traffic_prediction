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

### Data Elaboration

### Analysis of the Capture files

### Prediction with Prophet

### Observations and notes


