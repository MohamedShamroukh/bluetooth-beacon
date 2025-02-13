# Bluetooth Beacon Scanner

This Python script acts as a Bluetooth Low Energy (BLE) scanner, detecting the number of unique Bluetooth devices within a specified distance. It leverages the `Bleak` library for BLE scanning and estimates device distances based on Received Signal Strength Indicator (RSSI). The script continuously scans, filters devices beyond a defined range (default: 5 meters), updates device information, and calculates the duration each device has been detected (dwell time).  It can also estimate the number of people in proximity by considering devices within a short distance of each other as the same person.

## Features

*   **BLE Scanning:** Uses `Bleak` to scan for Bluetooth Low Energy devices.
*   **Distance Estimation:** Estimates device distance based on RSSI values.
*   **Proximity Calculation:** Determines if two devices are close to each other.
*   **Device Filtering:** Filters out devices beyond a configurable distance threshold.
*   **Dwell Time Calculation:** Calculates how long each unique device has been detected.
*   **People Counting Estimation**: Estimates the number of unique people in proximity.
*   **Real-time Reporting:** Prints the number of unique devices/estimated people within the defined range at regular intervals.
*   **Summary Report:** Provides a summary of detected devices, including their MAC address, RSSI, estimated distance, detection count, dwell time, and first/last seen timestamps when the script is stopped.
*   **Pretty Table Output:** Uses `PrettyTable` for a visually appealing summary report.

## Requirements

*   Python 3.7+
*   Bleak library: `pip install bleak`
*   PrettyTable library: `pip install prettytable`

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd bluetooth-beacon
    ```

2.  Install the required libraries:

    ```bash
    pip install bleak prettytable
    ```

## Usage

Run the script:

```bash
python bluetooth-beacon.py
Use code with caution.
Markdown
The script will start scanning for BLE devices and print the estimated number of people in proximity every few seconds. Press Ctrl+C to stop the scan. After stopping, the script will print a summary table of detected devices and their dwell times.

Configuration
The script can be configured using the following parameters within the code:

scan_interval: The interval (in seconds) between each scan (default: 5 seconds).

max_distance_threshold: The maximum distance (in meters) to consider devices (default: 5 meters).

threshold: The proximity range for people counting (default 1.5 meters). If 2 devices are less than 1.5 meters they are considered to be the same person

Example:
To change the scan interval to 10 seconds and the maximum distance threshold to 3 meters, modify the continuous_scan function like this:

async def continuous_scan(scan_interval=10, max_distance_threshold=3):
Use code with caution.
Python
Code Explanation
estimate_distance(rssi, tx_power=-59): Estimates the distance from the RSSI value. The tx_power is the RSSI value at 1 meter from the device. You may need to calibrate this value for your environment and specific beacons.

is_within_proximity(device1, device2, threshold=1.5): Determines if two devices are within the specified distance threshold of each other.

calculate_dwell_time(first_seen, last_seen): Calculates the dwell time (in seconds) between the first and last detection of a device.

scan_for_devices(scanner, scan_time=5): Scans for BLE devices for a specified scan_time. It updates the unique_devices dictionary with new device information or updates existing device data. It also filters the devices based on the maximum distance threshold.

continuous_scan(scan_interval=5, max_distance_threshold=5): Continuously scans for BLE devices at a specified interval. It handles proximity filtering to estimate the number of unique people nearby.

main(): The main function that runs the continuous scan and displays the results in a pretty table when the script is stopped.

Output
The script provides two types of output:

Real-time Output:

During the continuous scan, the script prints the estimated number of people in proximity:

Estimated people count (devices within 1.5 meter considered the same): 3
Use code with caution.
Summary Report:

When the scan is stopped (using Ctrl+C), the script prints a summary table similar to this:

Final list of detected devices with dwelling times:
+----+---------------------+---------+-------+-----------------------+------+---------------------+---------------------+---------------------+
| ID |         MAC         |  Name   | Count | Approx. Distance (m)  | RSSI |     First Seen      |      Last Seen      | Dwelling Time (s) |
+----+---------------------+---------+-------+-----------------------+------+---------------------+---------------------+---------------------+
| 1  | XX:XX:XX:XX:XX:XX | MyDevice1 |   5   |         2.35        |  -70 | 2024-10-27 10:00:00 | 2024-10-27 10:00:25 |         25.0        |
| 2  | YY:YY:YY:YY:YY:YY | Unknown |   3   |         1.80        |  -65 | 2024-10-27 10:00:05 | 2024-10-27 10:00:20 |         15.0        |
| 3  | ZZ:ZZ:ZZ:ZZ:ZZ:ZZ | MyDevice2 |   2   |         4.12        |  -75 | 2024-10-27 10:00:10 | 2024-10-27 10:00:25 |         15.0        |
+----+---------------------+---------+-------+-----------------------+------+---------------------+---------------------+---------------------+

Average Dwelling Time: 18.33 seconds
Use code with caution.
The table includes:

ID: A unique identifier for each detected device.

MAC: The MAC address of the Bluetooth device.

Name: The name of the Bluetooth device (if available).

Count: The number of times the device was detected during the scan.

Approx. Distance (m): The estimated distance of the device in meters.

RSSI: The Received Signal Strength Indicator.

First Seen: The timestamp when the device was first detected.

Last Seen: The timestamp when the device was last detected.

Dwelling Time (s): The total time the device was detected (in seconds).

It also calculates and displays the average dwelling time for all detected devices.

Calibration
The accuracy of the distance estimation depends on the tx_power value used in the estimate_distance function. The default value of -59 is a general approximation and may not be accurate for all devices and environments. To improve accuracy, calibrate the tx_power value for your specific use case:

Place a known Bluetooth beacon (or device) at a distance of 1 meter from the scanning device.

Run the script and observe the RSSI value reported for that beacon.

Use the average RSSI value observed at 1 meter as the new tx_power value in the estimate_distance function.

Limitations
Distance Estimation: Distance estimation based on RSSI is inherently imprecise and can be affected by environmental factors like walls, interference, and device orientation.

Bluetooth Permissions: Requires appropriate Bluetooth permissions on the operating system.

Battery Consumption: Continuous Bluetooth scanning can consume significant battery power.

Contributing
Contributions are welcome! Please submit pull requests with bug fixes, improvements, or new features.

License
MIT License
