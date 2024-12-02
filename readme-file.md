# System Sleep Prevention Utility

## Overview

This Python script provides a utility to temporarily prevent your Windows system from going to sleep. It allows you to:
- Specify a custom duration for keeping the system awake
- Use a kill switch to manually restore sleep settings
- Run in the background without high CPU usage

## Features

- Prevent system sleep for a specified duration
- Customizable kill switch (Ctrl+Shift+Q by default)
- Minimal CPU impact
- Simple command-line interface
- Thread-based implementation for smooth operation

## Prerequisites

- Python 3.x
- Windows Operating System (uses Windows-specific API calls)
- `keyboard` module

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/system-sleep-prevention.git
   cd system-sleep-prevention
   ```

2. Install required dependencies:
   ```bash
   pip install keyboard
   ```

## Usage

Run the script and enter the number of minutes you want to prevent system sleep:

```bash
python prevent_sleep.py
```

### Example

```
Enter the number of minutes to prevent system sleep: 120
System sleep prevented for 120 minutes.
Press ctrl+shift+q to restore sleep settings.
```

### Kill Switch

- By default, pressing `Ctrl+Shift+Q` will immediately restore system sleep settings
- This allows you to quickly cancel the sleep prevention

## Customization

You can modify the following in the script:
- Change the kill switch key combination
- Adjust the sleep prevention logic

## Important Notes

- This script uses Windows-specific API calls and will only work on Windows
- Requires administrative privileges to modify system sleep settings
- Use the kill switch or wait for the specified duration to restore normal sleep behavior

## Potential Use Cases

- Preventing screen timeout during presentations
- Keeping system awake during long downloads or computations
- Maintaining system state during extended tasks

## Dependencies

- `ctypes`: For Windows API calls
- `time`: For duration tracking
- `threading`: For background task management
- `keyboard`: For kill switch functionality

## License

[Choose an appropriate license and add it here]

## Contributions

Contributions, issues, and feature requests are welcome!

## Disclaimer

Use this script responsibly. Preventing system sleep for extended periods can impact battery life and system performance.