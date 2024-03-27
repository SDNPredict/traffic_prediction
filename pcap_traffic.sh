pingall

h1 for file in dataset/h1/*.pcap; do tcpreplay --loop=5000 --loopdelay-ms=5000 -i h1-eth0 --pps=10 $file & done

h2 for file in dataset/h2/*.pcap; do tcpreplay --loop=5000 --loopdelay-ms=5000 -i h2-eth0 --pps=8 $file & done

h3 for file in dataset/h3/*.pcap; do tcpreplay --loop=5000 --loopdelay-ms=5000 -i h3-eth0 --pps=5 $file & done

h4 for file in dataset/h4/*.pcap; do tcpreplay --loop=5000 --loopdelay-ms=5000 -i h4-eth0 --pps=12 $file & done
