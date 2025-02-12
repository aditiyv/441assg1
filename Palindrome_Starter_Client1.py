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
    return ''.join(chr(ord(char) ^ key) for char in data)

def start_client():
    """ Start the client and connect to the server. """
    retries = 0

    while retries < MAX_RETRIES:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.settimeout(TIMEOUT)
                client_socket.connect((SERVER_HOST, SERVER_PORT))
                
                while True:
                    # Display the menu and get user input
                    print("\nMenu:")
                    print("1. Simple Palindrome Check")
                    print("2. Complex Palindrome Check")
                    print("3. Exit")
                    choice = input("Enter choice (1/2/3): ").strip()

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

                    # Encrypt the message before sending
                    encrypted_message = xor_encrypt_decrypt(message)
                    client_socket.send(encrypted_message.encode())

                    # Wait for server response
                    encrypted_response = client_socket.recv(1024).decode()

                    # Decrypt response from server
                    response = xor_encrypt_decrypt(encrypted_response)
                    print(f"Server response: {response}")

        except (socket.timeout, ConnectionRefusedError):
            retries += 1
            print(f"Connection attempt {retries}/{MAX_RETRIES} failed. Retrying...")
            time.sleep(2)  # Wait before retrying

    print("Failed to connect after multiple attempts. Exiting.")

if __name__ == "__main__":
    start_client()
