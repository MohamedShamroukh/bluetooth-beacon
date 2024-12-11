# bluetooth-beacon
bluetooth script that act as bluetooth scanner and detect the number of unique Bluetooth devices within a specific distance.
This Python script uses the Bleak library to scan for Bluetooth Low Energy (BLE) devices, estimate their distance based on RSSI, and filter out devices more than 5 meters away. It continuously scans, updates device information, and calculates how long each device has been detected. The script prints the number of unique devices within 5 meters at regular intervals and provides a summary of detected devices and their dwell times when stopped.
