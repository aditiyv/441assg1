import socket
import time

# Server configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
MAX_RETRIES = 3
TIMEOUT = 5  # seconds
ENCRYPTION_KEY = 5  # Simple XOR key for encryption/decryption

def xor_encrypt_decrypt(data, key=ENCRYPTION_KEY):
    """Encrypts or decrypts data using XOR cipher."""
    return ''.join(chr(ord(char) ^ key) for char in data) # XOR operation for encryption/decryption

def start_client():
    """ Start the client and connect to the server. """
    retries = 0

    while retries < MAX_RETRIES:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket: # Create a new socket
                client_socket.settimeout(TIMEOUT) # Set a timeout - 5 secs for the connection as per assg req
                client_socket.connect((SERVER_HOST, SERVER_PORT)) # Connect to the server
                
                while True:
                    # Display the menu and get user input
                    print("\nMenu:")
                    print("1. Simple Palindrome Check")
                    print("2. Complex Palindrome Check")
                    print("3. Exit")
                    choice = input("Enter choice (1/2/3): ").strip()

                    # Process user choice
                    if choice == '1':
                        input_string = input("Enter the string to check: ") 
                        message = f"simple|{input_string}"
                    elif choice == '2':
                        input_string = input("Enter the string to check: ")
                        message = f"complex|{input_string}"
                    elif choice == '3':
                        print("Exiting the client...")
                        return
                    else:
                        print("Invalid choice, please try again.")
                        continue

                    encrypted_message = xor_encrypt_decrypt(message) # Encrypt the message
                    client_socket.send(encrypted_message.encode()) # Send the encrypted message to the server

                    encrypted_response = client_socket.recv(1024).decode() # Receive encrypted response from server

                    response = xor_encrypt_decrypt(encrypted_response) # Decrypt the response
                    print(f"Server response: {response}")

        except (socket.timeout, ConnectionRefusedError): # Handle connection errors
            retries += 1 # Increment the retry count
            print(f"Connection attempt {retries}/{MAX_RETRIES} failed. Retrying...") # Retry message - only thrice
            time.sleep(2)  # Wait before retrying

    print("Failed to connect after multiple attempts. Exiting.") # Print message if connection fails after retries

if __name__ == "__main__":
    start_client() # Start the client
