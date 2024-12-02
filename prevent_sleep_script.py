import ctypes
import time
import threading
import keyboard

class SleepPreventionManager:
    """
    A utility class to prevent system sleep on Windows.
    
    This class provides methods to temporarily disable system sleep 
    and allows users to set a custom duration and kill switch.
    
    Attributes:
        ES_CONTINUOUS (int): Constant for continuous execution state.
        ES_SYSTEM_REQUIRED (int): Constant to prevent system sleep.
        ES_DISPLAY_REQUIRED (int): Constant to keep display on.
        keep_preventing_sleep (bool): Flag to control sleep prevention.
        kill_switch_keys (list): Key combination to cancel sleep prevention.
    """

    def __init__(self):
        """
        Initialize the SleepPreventionManager with Windows API constants.
        
        Sets up the necessary Windows API constants and initializes 
        sleep prevention control flags.
        """
        # Windows API constants
        self.ES_CONTINUOUS = 0x80000000
        self.ES_SYSTEM_REQUIRED = 0x00000001
        self.ES_DISPLAY_REQUIRED = 0x00000002
        
        # Flag to control sleep prevention
        self.keep_preventing_sleep = False
        
        # Kill switch key combination
        self.kill_switch_keys = ['ctrl', 'shift', 'q']

    def prevent_system_sleep(self, duration_minutes):
        """
        Prevent the system from sleeping for a specified duration.
        
        Uses Windows API to keep the system and display active.
        Provides user feedback and allows cancellation via kill switch.
        
        Args:
            duration_minutes (int): Number of minutes to prevent system sleep.
        
        Raises:
            Exception: If there's an error preventing system sleep.
        """
        try:
            # Prevent system sleep using Windows API
            ctypes.windll.kernel32.SetThreadExecutionState(
                self.ES_CONTINUOUS | self.ES_SYSTEM_REQUIRED | self.ES_DISPLAY_REQUIRED
            )
            
            print(f"System sleep prevented for {duration_minutes} minutes.")
            print(f"Press {'+'.join(self.kill_switch_keys)} to restore sleep settings.")
            
            self.keep_preventing_sleep = True
            start_time = time.time()
            
            # Monitoring loop
            while self.keep_preventing_sleep:
                # Check if duration has elapsed
                if time.time() - start_time >= (duration_minutes * 60):
                    break
                
                # Small sleep to prevent high CPU usage
                time.sleep(1)
        
        except Exception as e:
            print(f"An error occurred: {e}")
        
        finally:
            # Restore sleep settings regardless of how the loop exits
            self.restore_sleep_settings()

    def restore_sleep_settings(self):
        """
        Restore default system sleep behavior.
        
        Uses Windows API to reset the system's sleep state.
        
        Raises:
            Exception: If there's an error restoring sleep settings.
        """
        try:
            # Reset thread execution state to default
            ctypes.windll.kernel32.SetThreadExecutionState(self.ES_CONTINUOUS)
            print("System sleep settings restored.")
            self.keep_preventing_sleep = False
        except Exception as e:
            print(f"Error restoring sleep settings: {e}")

    def setup_kill_switch(self):
        """
        Set up a kill switch to manually stop sleep prevention.
        
        Registers a keyboard shortcut to immediately restore 
        system sleep settings.
        """
        def kill_sleep_prevention():
            """
            Callback function to stop sleep prevention when kill switch is pressed.
            """
            if self.keep_preventing_sleep:
                print("\nKill switch activated. Restoring sleep settings...")
                self.keep_preventing_sleep = False
        
        # Register the kill switch key combination
        keyboard.add_hotkey('+'.join(self.kill_switch_keys), kill_sleep_prevention)

def main():
    """
    Main function to run the sleep prevention utility.
    
    Creates a SleepPreventionManager, sets up the kill switch,
    and starts sleep prevention for a user-specified duration.
    
    Handles user input and potential exceptions.
    """
    try:
        # Create sleep prevention manager
        sleep_manager = SleepPreventionManager()
        
        # Set up kill switch
        sleep_manager.setup_kill_switch()
        
        # Get duration from user input
        duration = int(input("Enter the number of minutes to prevent system sleep: "))
        
        # Create a thread to prevent sleep
        sleep_prevention_thread = threading.Thread(
            target=sleep_manager.prevent_system_sleep, 
            args=(duration,), 
            daemon=True
        )
        
        # Start the thread
        sleep_prevention_thread.start()
        
        # Wait for the thread to complete
        sleep_prevention_thread.join()
    
    except ValueError:
        print("Please enter a valid number of minutes.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    finally:
        # Ensure sleep settings are restored
        try:
            sleep_manager.restore_sleep_settings()
        except:
            pass

if __name__ == "__main__":
    # Requires keyboard module - install via: pip install keyboard
    main()