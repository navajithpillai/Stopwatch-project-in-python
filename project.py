import time
import threading
import keyboard  # For capturing keyboard input

# Initialize time variables
counter = 0
running = False
laps = []

# Lock to manage console output while updating the timer and taking input
console_lock = threading.Lock()

# Function to update the stopwatch
def update_timer():
    global counter, running
    while running:
        minutes, seconds = divmod(counter, 60)
        time_string = f"{minutes:02d}:{seconds:02d}"

        # Lock the console to prevent interference with input
        with console_lock:
            print(f"\r{time_string}", end="")

        time.sleep(1)
        counter += 1

# Start the stopwatch
def start():
    global running
    if not running:
        running = True
        threading.Thread(target=update_timer, daemon=True).start()

# Stop the stopwatch
def stop():
    global running
    running = False

# Record lap times
def lap():
    global counter
    if running:
        minutes, seconds = divmod(counter, 60)
        lap_time = f"Lap {len(laps) + 1}: {minutes:02d}:{seconds:02d}"
        laps.append(lap_time)

        # Lock the console to print the lap time
        with console_lock:
            print("\n" + lap_time)

# Reset the stopwatch
def reset():
    global counter, running, laps
    running = False
    counter = 0
    laps.clear()

    # Lock the console to reset the display
    with console_lock:
        print("\r00:00")

# Function to capture keyboard commands without blocking the stopwatch
def capture_commands():
    while True:
        if keyboard.is_pressed('s'):
            print("\nStart pressed")
            start()
        elif keyboard.is_pressed('t'):
            print("\nStop pressed")
            stop()
        elif keyboard.is_pressed('l'):
            print("\nLap pressed")
            lap()
        elif keyboard.is_pressed('r'):
            print("\nReset pressed")
            reset()
        elif keyboard.is_pressed('q'):
            print("\nQuit pressed")
            stop()
            break
        time.sleep(0.1)

# Main loop to run the program
def main():
    print("Press 's' to start, 't' to stop, 'l' for lap, 'r' to reset, 'q' to quit.")
    capture_commands()

if __name__ == "__main__":
    main()