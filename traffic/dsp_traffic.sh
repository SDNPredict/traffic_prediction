pingall

h1 python3 ./traffic.py 10.0.0.2 -w sine -p 30 -d 180 &

h2 python3 ./traffic.py 10.0.0.1 -w triangular -p 30 -d 180 &

h3 python3 ./traffic.py 10.0.0.4 -w sawtooth -p 30 -d 180 &

h4 python3 ./traffic.py 10.0.0.3 -w square -p 30 -d 180 &
