import socket 
import struct
import json

# Set up a TCP socket to receive the AIS data
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 5555))
sock.listen(1)
conn, addr = sock.accept()
print('Connected by', addr)

# Set up a connection to the online AIS decoder
decoder_url = 'http://ais.tbsalling.dk/decode'

# Set up a connection to the data store
# (in this example, we'll use a simple in-memory dictionary)
data_store = {}

while True:
  # Receive and decode the AIS message
  raw_data = conn.recv(1024)
  if not raw_data: break
  decoded_data = json.loads(raw_data.decode('utf-8'))

  # Extract the relevant fields from the AIS message
  mmsi = decoded_data['MMSI']
  vessel_name = decoded_data['Vessel Name']
  destination = decoded_data['Destination']

  # Store the data in the data store
  data_store[mmsi] = {
      'vessel_name': vessel_name,
      'destination': destination
  }

# Close the connections
conn.close()
sock.close()

# Print the contents of the data store
print(data_store)
