from CythonCommunicator import *
from global_vars import *

import time

def main():
    comm = CythonCommunicator(python_port=PYTHON_PORT, c_port=C_PORT)
    print("[+] Starting communication loop (Press Ctrl+C to exit)")

    try:
        while True:
            # Receive message
            comm.receive_message()

            # Get input from the user
            user_message = input("Enter a message to send: ")
            comm.send_message(user_message)
            
            time.sleep(SLEEP_TIME)
    
    except KeyboardInterrupt:
        print("\n[+] Exiting...")
    
    finally:
        comm.cleanup()

if __name__ == "__main__":
    main()
