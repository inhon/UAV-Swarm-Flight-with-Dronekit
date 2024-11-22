import threading

class RepeatTimer(threading.Timer):
    '''
    Usage: 
    timer = RepeatTimer(5, <name of function>, (args,))
    timer.start()
    timer.cancel()
    '''
    def run(self):
        """
        Overridden method to repeatedly call the target function at the given interval.
        """
        while not self.finished.wait(self.interval):  # Waits for the interval or until canceled
            self.function(*self.args, **self.kwargs)  # Call the target function

# Example function to send a message
def sendMsg(vehicle, client):
    print(f"Sending message to {client} with info: COORDINATES")
    # You can replace the print with the actual functionality, e.g., vehicle.sendInfo(client, "COORDINATES")

# Example usage
if __name__ == "__main__":
    # Create a RepeatTimer to call sendMsg every 5 seconds
    vehicle = "Car"  # Example vehicle object
    client = "Client_123"  # Example client ID
    timer = RepeatTimer(5, sendMsg, (vehicle, client))

    # Start the timer to repeatedly call sendMsg every 5 seconds
    timer.start()

    # Run for some time and then stop
    try:
        # Let it run for 20 seconds before canceling
        threading.Event().wait(20)
    finally:
        timer.cancel()  # Stop the timer after 20 seconds
