# Import required dependencies
import json
import sys
import time
from socket import *

# Define friendly keys constants for stats
RECV = 'Received Objects'
LAST = 'Last Object Number'
MISS = 'Missing Objects'
AVGT = 'Average Send Time'
OART = 'Objects Arrival Time'

# Define a function for getting curr time in ms
curr_time = lambda: int(round(time.time() * 1000))

# Define a dictionary with stats per client
stats = {}

# Define server port (5000 by default)
port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

# Define socket buffer size
buffer_size = 2048

# Create the UDP socket object at the specified port
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', port))

# Print a friendly message indicating everything is OK
print 'Receiving data happily at port:', port

# Start listening data from any client
while True:
	# Get the client message and address
	message, client_addr = server_socket.recvfrom(buffer_size)

	# Try to parse the message as a python dict
	# If message is not a valid json, just go on
	try:
		message = json.loads(message)
	except:
		continue

	# Create new stats object if necessary
	curr_stat = stats.get(client_addr, {})

	# Calculate arrival time of curr message
	arrival_time = curr_time() - message['timestamp']

	# Calculate new client stats
	received_objects = curr_stat.get(RECV, 0) + 1
	last_object = max(curr_stat.get(LAST, 0), message['object_number'])
	missing_objects = last_object - received_objects
	avg_sent_time = curr_stat.get(AVGT, 0) + arrival_time

	objects = curr_stat.get(OART, [])
	objects.append((message['object_number'], arrival_time))

	# Update client stats with new data
	stats[client_addr] = {
		RECV: received_objects,
		LAST: last_object,
		MISS: missing_objects,
		AVGT: avg_sent_time,
		OART: objects
	}

	# Write new stats to client file
	with open('./%s:%d.txt' % (client_addr[0], client_addr[1]), 'w') as f:
		f.write('%s: %d\n' % (RECV, received_objects))
		f.write('%s: %d\n' % (MISS, missing_objects))
		f.write('%s: %.2fms\n' % (AVGT, float(avg_sent_time)/float(received_objects)))

		f.write('\nObjects arrival times...\n')
		for curr_obj in sorted(objects):
			f.write('%d: %dms\n' % curr_obj)
