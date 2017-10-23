# Import required dependencies
import json
import sys
import time
from flask import request
from flask import Flask
from socket import *

# Define a function for getting curr time in ms
curr_time = lambda: int(round(time.time() * 1000))

# Initialize a new flask app
app = Flask(__name__)

# Define an endpoint for showing the interface
@app.route('/', methods=['GET'])
def index():
	return app.send_static_file('index.html')

# Define an endpoint for sending messages
@app.route('/', methods=['POST'])
def send_messages():
	# Create the UDP socket object
	client_socket = socket(AF_INET, SOCK_DGRAM)

	# Read the parameters for the messages
	total_messages = int(request.form['total_messages'])
	server_ip = request.form['server_ip']
	server_port = int(request.form['server_port'])

	# Send the specified number of messages
	for i in range(total_messages):
		# Build the json message to be sent
		message = json.dumps({
			'object_number': i+1,
			'timestamp': curr_time()
		})

		# Send the message through the socket
		client_socket.sendto(message, (server_ip, server_port))

	# Close the UDP socket
	client_socket.close()

	return app.send_static_file('index.html')

# Start running the flask app
app.run(host='0.0.0.0')
