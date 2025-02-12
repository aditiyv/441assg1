import socket
import threading
import logging
from collections import Counter

# Set up basic logging configuration
logging.basicConfig(filename='server_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Constants for the server configuration
HOST = 'localhost'
PORT = 12345
ENCRYPTION_KEY = 5  # Simple XOR key for encryption/decryption

def xor_encrypt_decrypt(data, key=ENCRYPTION_KEY):
    """Encrypts or decrypts data using XOR cipher."""
    return ''.join(chr(ord(char) ^ key) for char in data)

def handle_client(client_socket, client_address):
    """ Handle incoming client requests. """
    logging.info(f"Connection from {client_address}")
    
    try:
        while True:
            # Receive encrypted data from client
            encrypted_data = client_socket.recv(1024).decode()
            if not encrypted_data:  # Client has closed the connection
                break

            # Decrypt received message
            request_data = xor_encrypt_decrypt(encrypted_data)
            logging.info(f"Received request: {request_data}")

            # Process the request
            response = process_request(request_data)

            # Encrypt response before sending
            encrypted_response = xor_encrypt_decrypt(response)
            client_socket.send(encrypted_response.encode())

            logging.info(f"Sent response: {response}")
    finally:
        client_socket.close()
        logging.info(f"Closed connection with {client_address}")

def process_request(request_data):
    """ Process the client's request and generate a response. """
    check_type, input_string = request_data.split('|')
    # Remove non-alphanumeric characters and convert to lowercase
    input_string = ''.join(e for e in input_string if e.isalnum()).lower()

    if check_type == 'simple':
        result = is_palindrome(input_string)
        return f"Is palindrome: {result}"
    elif check_type == 'complex':
        can_form, complexity_score = can_rearrange_to_palindrome(input_string)
        return f"Can form a palindrome: {can_form}, Complexity score: {complexity_score}"

def is_palindrome(input_string):
    """ Check if the given string is a palindrome. """
    return input_string == input_string[::-1]

def can_rearrange_to_palindrome(input_string):
    """ Check if the given string can be rearranged into a palindrome and calculate the minimum swaps. """
    char_counts = Counter(input_string)
    odd_count = sum(1 for count in char_counts.values() if count % 2 != 0)

    # If more than 1 character has an odd count, it cannot be rearranged into a palindrome.
    if odd_count > 1:
        return False, -1  # Complexity score not applicable

    # Calculate minimum swaps needed to form a palindrome.
    swaps = min_swaps_to_palindrome(list(input_string))
    return True, swaps

def min_swaps_to_palindrome(s):
    """ Compute the minimum number of swaps needed to convert a string into a palindrome. """
    s = s[:]  # Copy the list to avoid modifying the original
    swaps = 0
    l, r = 0, len(s) - 1

    while l < r:
        if s[l] == s[r]:
            l += 1
            r -= 1
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
    """ Start the server and listen for incoming connections. """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        logging.info(f"Server started and listening on {HOST}:{PORT}")
        
        while True:
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == '__main__':
    start_server()
