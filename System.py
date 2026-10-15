import os
import csv
import cv2
import numpy as np
import subprocess
import datetime
import serial
import time


BASE = os.path.dirname(os.path.abspath(__file__))

IMAGES = os.path.join(BASE, "images")
DATA = os.path.join(BASE, "data")
CSV = os.path.join(DATA, "clover.csv")


os.makedirs(IMAGES, exist_ok=True)
os.makedirs(DATA, exist_ok=True)


def capture_image(image_path):

    subprocess.run([
        "rpicam-still",
        "-o", image_path,
        "--width", "640",
        "--height", "480",
        "--nopreview"
    ])


def analyze_green_area(image_path):

    img = cv2.imread(image_path)

    if img is None:
        print("Image error")
        return 0

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)

    green_pixels = cv2.countNonZero(mask)

    return green_pixels


def read_arduino():

    try:

        ser = serial.Serial('/dev/ttyUSB0',9600,timeout=5)

        time.sleep(2)

        line = ser.readline().decode().strip()

        ser.close()

        if line:

            parts = line.split(",")

            if len(parts) == 4:

                soil = int(parts[0])
                light = int(parts[1])
                temp = float(parts[2])
                humidity = float(parts[3])

                return soil, light, temp, humidity

    except Exception as e:

        print("Serial error:", e)

    return None,None,None,None

def save_data(date,area,soil,light,temp,humidity):

    file_exists = os.path.isfile(CSV)

    with open(CSV,'a',newline='') as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "Date",
                "Green_Pixels",
                "Soil",
                "Light",
                "Temp",
                "Humidity"
            ])

        writer.writerow([
            date,
            area,
            soil,
            light,
            temp,
            humidity
        ])

def main():

    print("Starting system...")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    image_filename = f"clover_{timestamp}.jpg"

    image_path = os.path.join(IMAGES,image_filename)

    # Capture image

    capture_image(image_path)

    time.sleep(2)

    # Analyze plant

    green_area = analyze_green_area(image_path)

    # Read sensors

    soil,light,temp,humidity = read_arduino()

    # Save data

    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    save_data(today,green_area,soil,light,temp,humidity)

    print("Saved:",today)
    print("Image:",image_filename)
    print("Green Pixels:",green_area)
    print("Soil:",soil)
    print("Light:",light)
    print("Temp:",temp)
    print("Humidity:",humidity)

if __name__ == "__main__":
    main()