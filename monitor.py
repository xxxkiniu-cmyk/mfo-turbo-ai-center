import psutil
import time

while True:
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()
    temp = "Brak dostępu"
    
    temps = psutil.sensors_temperatures()
    if temps and 'coretemp' in temps:
        temp = f"{temps['coretemp'][0].current}°C"

    if ram > 85:
        print(f"Ostrzeżenie: RAM to {ram}%! CPU: {cpu}%, Temp: {temp}")
    else:
        print(f"System OK. RAM: {ram}%, CPU: {cpu}%, Temp: {temp}")
    time.sleep(1)
