#!/bin/bash

HOSTS=4

for ((i = 1; i <= $HOSTS; i++)); do
  echo "starting host_$i"
  sudo tcpdump -i s1-eth${i} -w ../dumps/h${i}_traffic.pcap -U &
done

