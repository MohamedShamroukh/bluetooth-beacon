import asyncio
from bleak import BleakScanner
import math
from datetime import datetime
from prettytable import PrettyTable

# Dictionary to store unique devices and their information
unique_devices = {}

def estimate_distance(rssi, tx_power=-59):
    """Estimate distance from RSSI value."""
    if rssi == 0:
        return -1  # Unknown distance
    ratio = rssi / tx_power
    if ratio < 1.0:
        return pow(ratio, 10)
    else:
        return 0.89976 * pow(ratio, 7.7095) + 0.111

def is_within_proximity(device1, device2, threshold=1.5):
    """Determine if two devices are within a given distance threshold."""
    return abs(device1["distance"] - device2["distance"]) <= threshold

def calculate_dwell_time(first_seen, last_seen):
    """Calculate the dwelling time in seconds."""
    first_seen_time = datetime.strptime(first_seen, "%Y-%m-%d %H:%M:%S")
    last_seen_time = datetime.strptime(last_seen, "%Y-%m-%d %H:%M:%S")
    return (last_seen_time - first_seen_time).total_seconds()

async def scan_for_devices(scanner, scan_time=5):
    detected_devices = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    devices = await scanner.discover(timeout=scan_time)

    for device in devices:
        mac = device.address
        rssi = device.rssi  # Correct way to access RSSI
        distance = estimate_distance(rssi)

        if distance <= 5:  # Filter by distance
            # Add new device or update existing device data
            if mac not in unique_devices:
                unique_devices[mac] = {
                    "id": len(unique_devices) + 1,
                    "mac": mac,
                    "first_seen": now,
                    "last_seen": now,
                    "name": device.name or "Unknown",
                    "distance": distance,
                    "rssi": rssi,
                    "count": 1
                }
                detected_devices.append(unique_devices[mac])  # Add new device to scan list

            else:
                # Update existing device
                unique_devices[mac]["last_seen"] = now
                unique_devices[mac]["distance"] = distance
                unique_devices[mac]["rssi"] = rssi
                unique_devices[mac]["count"] += 1
                detected_devices.append(unique_devices[mac])

    return detected_devices

async def continuous_scan(scan_interval=5, max_distance_threshold=5):
    """Continuously scans for BLE devices."""

    print("Starting continuous BLE scan. Press Ctrl+C to stop.")
    scanner = BleakScanner()
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Scan started at: {start_time}")

    try:
        while True:
            detected_devices = await scan_for_devices(scanner, scan_time=scan_interval)

            # Proximity filtering and people counting
            unique_people_count = 0
            counted_devices = set()
            for i, device in enumerate(detected_devices):
                if device["mac"] not in counted_devices and device['distance'] <= max_distance_threshold:
                    unique_people_count += 1
                    counted_devices.add(device["mac"])
                    for other_device in detected_devices[i + 1:]:
                        if other_device["mac"] not in counted_devices and other_device['distance'] <= max_distance_threshold:
                            if is_within_proximity(device, other_device):
                                counted_devices.add(other_device["mac"])

            print(f"\nEstimated people count (devices within 1.5 meter considered the same): {unique_people_count}\n")
            await asyncio.sleep(scan_interval)  # Use scan_interval for sleep

    except KeyboardInterrupt:
        print("\nStopping scan...")
        await scanner.stop() # Stop the scanner when KeyboardInterrupt is received
        return  # Exit cleanly

async def main():
    """Main function to run the scan and display results."""
    try:
       await continuous_scan()
    except asyncio.CancelledError:
        print("\nScan cancelled.") # Handle asyncio.CancelledError
    finally:
        # Ensure this block always runs to print summary
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Scan ended at: {end_time}")

        # Display results in a pretty table
        table = PrettyTable()
        table.field_names = ["ID", "MAC", "Name", "Count", "Approx. Distance (m)", "RSSI", "First Seen", "Last Seen", "Dwelling Time (s)"]
        total_dwell_time = 0

        for mac, info in unique_devices.items():
           dwell_time = calculate_dwell_time(info['first_seen'], info['last_seen'])
           total_dwell_time += dwell_time
           table.add_row([info['id'], info['mac'], info['name'], info['count'], f"{info['distance']:.2f}", info['rssi'], info['first_seen'], info['last_seen'], dwell_time])

        print("\nFinal list of detected devices with dwelling times:")
        print(table)

        average_dwell_time = total_dwell_time / len(unique_devices) if unique_devices else 0
        print(f"\nAverage Dwelling Time: {average_dwell_time:.2f} seconds")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program stopped manually.")
