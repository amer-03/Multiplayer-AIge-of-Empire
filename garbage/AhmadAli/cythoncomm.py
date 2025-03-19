import socket
import select
import time

class CythonCommunicator:
    def __init__(self, recv_port, send_port, send_ip="127.0.0.1"):
        """Initialize the communicator with specified ports and IP.

        Args:
            recv_port (int): Port to listen on
            send_port (int): Port to send to
            send_ip (str): IP address to send to (default: 127.0.0.1)
        """
        self.recv_port = recv_port
        self.send_port = send_port
        self.send_ip = send_ip
        self.send_addr = (send_ip, send_port)
        self.buffer_size = 1024


        self.last_send_time = 0
        self.message_interval = 0.5  # seconds between messages

        # Create and configure socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', recv_port))
        self.sock.setblocking(False)

        print(f"[+] Initialized communicator (recv_port: {recv_port}, send_port: {send_port}, send_ip: {send_ip})")

    def send_message(self, message):
        """Send a message to the configured address.

        Args:
            message (str): Message to send

        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        try:
            if isinstance(message, str):
                message = message.encode('utf-8')
            self.sock.sendto(message, self.send_addr)
            print(f"[+] Sent: {message.decode() if isinstance(message, bytes) else message}")
            return True

        except Exception as e:
            print(f"[-] Send failed: {str(e)}")
            return False

    def receive_message(self):
        """Receive a message (non-blocking).

        Returns:
            tuple: (message, address) if a message was received, (None, None) otherwise
        """
        try:
            ready = select.select([self.sock], [], [], 0)
            if ready[0]:
                data, addr = self.sock.recvfrom(self.buffer_size)
                print(f"[+] Received: {data.decode()} from {addr}")
                return data.decode(), addr
        except Exception as e:
            if not isinstance(e, BlockingIOError):
                print(f"[-] Receive failed: {str(e)}")
        return None, None

    def should_send_message(self):
        """Check if it's time to send a new message.

        Returns:
            bool: True if it's time to send a new message, False otherwise
        """
        current_time = time.time()
        if current_time - self.last_send_time >= self.message_interval:
            self.last_send_time = current_time
            return True
        return False

    def cleanup(self):
        """Close the socket and clean up resources."""
        if hasattr(self, 'sock'):
            self.sock.close()
            print("[+] Communicator cleaned up")

    def __del__(self):
        """Destructor to ensure the socket is closed."""
        self.cleanup()


def main():
    """Main function to run the communication loop."""
    # Initialize communicator (listening on 50000, sending to 50001)
    comm = CythonCommunicator(recv_port=50000, send_port=50001)

    print("[+] Starting communication loop (Press Ctrl+C to exit)")

    try:
        while True:
            # Check for received messages
            comm.receive_message()

            # Send periodic message
            #if comm.should_send_message():
            comm.send_message("message from Python")

            # Sleep a little to prevent CPU hogging
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\n[+] Exiting...")
    finally:
        comm.cleanup()


if __name__ == "__main__":
    main()
