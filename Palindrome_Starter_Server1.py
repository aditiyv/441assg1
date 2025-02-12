import socket
import threading
import logging
from collections import Counter

# Set up basic logging configuration
# Configure logging to write to a file with a specific format
logging.basicConfig(filename='server_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Constants for the server configuration
HOST = 'localhost'  # Server will run on localhost
PORT = 12345  # Port number for the server
ENCRYPTION_KEY = 5  # Simple XOR key for encryption/decryption

def xor_encrypt_decrypt(data, key=ENCRYPTION_KEY):
    """Encrypts or decrypts data using XOR cipher with a given key """
    return ''.join(chr(ord(char) ^ key) for char in data) # XOR operation for encryption/decryption

def handle_client(client_socket, client_address):
    """ Handle incoming client requests and send responses """
    logging.info(f"Connection from {client_address}")  # Log the client connection
    
    try:
        while True:
            # Receive encrypted data from client
            encrypted_data = client_socket.recv(1024).decode()
            if not encrypted_data:  # Client has closed the connection
                break

            # Decrypt received message
            request_data = xor_encrypt_decrypt(encrypted_data)
            logging.info(f"Received request: {request_data}")  # Log the received request

            # Process the request
            response = process_request(request_data)

            # Encrypt response before sending
            encrypted_response = xor_encrypt_decrypt(response)  # Encrypt the response
            client_socket.send(encrypted_response.encode())  # Send the encrypted response to the client

            logging.info(f"Sent response: {response}")  # Log the sent response
    finally:
        client_socket.close()  # Close the client socket
        logging.info(f"Closed connection with {client_address}")  # Log the closed connection

def process_request(request_data):
    """ Process the client's request and generate a response """
    check_type, input_string = request_data.split('|')
    # Remove non-alphanumeric characters and convert to lowercase
    input_string = ''.join(e for e in input_string if e.isalnum()).lower()

    if check_type == 'simple':  # Check if the request is for a simple palindrome check
        result = is_palindrome(input_string)  # Determine if the input string is a palindrome
        return f"Is palindrome: {result}"  # Return the result as a formatted string
    elif check_type == 'complex':  # Check if the request is for a complex palindrome check
        can_form, complexity_score = can_rearrange_to_palindrome(input_string)  # Determine if the input string can be rearranged into a palindrome and calculate the complexity score
        return f"Can form a palindrome: {can_form}, Complexity score: {complexity_score}"  # Return the results as a formatted string

def is_palindrome(input_string):
    """ Check if the given string is a palindrome """
    return input_string == input_string[::-1]

def can_rearrange_to_palindrome(input_string):
    """ Check if the given string can be rearranged into a palindrome and calculate the minimum swaps """
    char_counts = Counter(input_string)  # Count the occurrences of each character in the input string
    odd_count = sum(1 for count in char_counts.values() if count % 2 != 0)  # Count how many characters have an odd number of occurrences

    if odd_count > 1: # If more than 1 character has an odd count, it cannot be rearranged into a palindrome.
        return False, -1  # Complexity score not applicable

    # Calculate minimum swaps needed to form a palindrome.
    swaps = min_swaps_to_palindrome(list(input_string))
    return True, swaps

def min_swaps_to_palindrome(s):
    """ Compute the minimum number of swaps needed to convert a string into a palindrome """
    s = s[:]  # Copy the list to avoid modifying the original
    swaps = 0  # Initialize swap count to 0
    l, r = 0, len(s) - 1  # Set left and right pointers

    while l < r:  # Loop until the pointers meet in the middle
        if s[l] == s[r]:  # If characters at both pointers are the same
            l += 1  # Move left pointer to the right
            r -= 1  # Move right pointer to the left
        else:
            # Find matching character for s[l] from the right
            match_index = r
            while match_index > l and s[match_index] != s[l]:
                match_index -= 1

            if match_index == l:
                # No matching character found – swap it towards the center
                s[l], s[l+1] = s[l+1], s[l]
                swaps += 1
            else:
                # Swap to bring the found character towards the right position
                s[match_index], s[r] = s[r], s[match_index]
                swaps += 1
                l += 1
                r -= 1

    return swaps

def start_server():
    """ Start the server and listen for incoming connections """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:  # Create a TCP/IP socket
        server_socket.bind((HOST, PORT))  # Bind the socket to the address and port
        server_socket.listen(5)  # Listen for incoming connections, with a backlog of 5
        logging.info(f"Server started and listening on {HOST}:{PORT}")  # Log that the server has started
        
        while True:
            client_socket, client_address = server_socket.accept()  # Accept a new client connection
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()  # Start a new thread to handle the client

if __name__ == '__main__':
    start_server() # Start the server
