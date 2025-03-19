import socket
import select
import time

class CythonCommunicator:
    def __init__(self, python_port, c_port, c_ip="127.0.0.1"):
        """Initialize the communicator with specified ports and IP"""
        self.python_port = python_port
        self.c_port = c_port
        self.c_ip = c_ip
        self.c_addr = (c_ip, c_port)
        self.buffer_size = 1024


        self.last_send_time = 0
        self.message_interval = 0.5  # seconds between messages

        # Create and configure socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', python_port))
        self.sock.setblocking(False)

        print(f"[+] Initialized communicator (python_port: {python_port}, c_port: {c_port}, c_ip: {c_ip})")

    def send_message(self, message):
        """Send a message to the configured address. """
        
        try:
            if isinstance(message, str):
                message = message.encode('utf-8')
            self.sock.sendto(message, self.c_addr)
            print(f"[+] Sent: {message.decode() if isinstance(message, bytes) else message}")
            return True

        except Exception as e:
            print(f"[-] Send failed: {str(e)}")
            return False

    def receive_message(self):
        """Receive a message (non-blocking)."""

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
        """Checks if it's time to send a new message. """
        current_time = time.time()
        if current_time - self.last_send_time >= self.message_interval:
            self.last_send_time = current_time
            return True
        return False

    def cleanup(self):
        if hasattr(self, 'sock'):
            self.sock.close()
            print("[+] Communicator cleaned up")

    def __del__(self):
        self.cleanup()


def main():
    comm = CythonCommunicator(python_port=50000, c_port=50001)
    print("[+] Starting communication loop (Press Ctrl+C to exit)")

    try:
        while True:
            comm.receive_message()
            comm.send_message("message from Python")
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\n[+] Exiting...")
    finally:
        comm.cleanup()


if __name__ == "__main__":
    main()
