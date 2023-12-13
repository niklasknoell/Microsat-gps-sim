# Microsat-gps-sim
Microsat engineering GNSS simulator


Task Distribution:
- Create trajectory in csv based on TLEs (Bas)
- gps-sdr-sim (Niklas)
- recompile gps-sdr-sim for longer runtimes (done locally, need to check on the machine in the lab) (Niklas)
- run the sdr to gnss receiver and record output in NMEA format (Maurits)
- parse NMEA format (Maurits)
- run the sdr to gnss receiver and record output in binary format (Mattias)
- parse binary format (Mattias)
- write analysis program to compare trajectory input and gnss receiver output, i.e. quantify error (Bas)
