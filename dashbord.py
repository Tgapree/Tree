import tkinter as tk
import serial 
import csv
import os
import datetime



CSV_PATH = "/home/coon/clover/data/clover.csv"
SERIAL_PORT = "/dev/ttyUSB0"


try:
    ser = serial.Serial(SERIAL_PORT,9600,timeout=1)
except:
    ser = None



def get_leaf():

    if not os.path.exists(CSV_PATH):
        return "--"

    with open(CSV_PATH) as f:
        data = list(csv.reader(f))

    if len(data) < 2:
        return "--"

    return data[-1][1]



def get_growth():

    if not os.path.exists(CSV_PATH):
        return "--"

    with open(CSV_PATH) as f:
        data = list(csv.reader(f))

    if len(data) < 3:
        return "--"

    today = int(data[-1][1])
    yesterday = int(data[-2][1])

    growth = ((today - yesterday) / yesterday) * 100

    return round(growth,2)




root = tk.Tk()
root.title("Clover Monitor")

root.geometry("480x320")
root.configure(bg="black")

title = tk.Label(
    root,
    text="CLOVER MONITOR",
    fg="lime",
    bg="black",
    font=("Arial",24,"bold")
)

title.pack(pady=5)

soil_label = tk.Label(root,font=("Arial",16),fg="white",bg="black")
soil_label.pack()

temp_label = tk.Label(root,font=("Arial",16),fg="white",bg="black")
temp_label.pack()

hum_label = tk.Label(root,font=("Arial",16),fg="white",bg="black")
hum_label.pack()

light_label = tk.Label(root,font=("Arial",16),fg="white",bg="black")
light_label.pack()

leaf_label = tk.Label(root,font=("Arial",16),fg="cyan",bg="black")
leaf_label.pack()

growth_label = tk.Label(root,font=("Arial",16),fg="yellow",bg="black")
growth_label.pack()

time_label = tk.Label(root,font=("Arial",12),fg="white",bg="black")
time_label.pack(pady=5)



def update():

    soil = "--"
    light = "--"
    temp = "--"
    hum = "--"

    if ser:

        try:

            line = ser.readline().decode().strip()

            if line:

                parts = line.split(",")

                if len(parts) == 4:

                    soil = parts[0]
                    light = parts[1]
                    temp = parts[2]
                    hum = parts[3]

        except:
            pass


    leaf = get_leaf()
    growth = get_growth()

    soil_label.config(text="Soil Moisture : " + str(soil))
    temp_label.config(text="Temperature : " + str(temp) + " C")
    hum_label.config(text="Humidity : " + str(hum) + " %")
    light_label.config(text="Light : " + str(light))

    leaf_label.config(text="Leaf Area : " + str(leaf))
    growth_label.config(text="Growth : " + str(growth) + " %")

    now = datetime.datetime.now().strftime("%H:%M:%S")
    time_label.config(text="Last Update : " + now)

    root.after(2000,update)


update()

root.mainloop()