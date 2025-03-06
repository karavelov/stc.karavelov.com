import subprocess
import time
import pymysql
import paho.mqtt.client as mqtt
import threading

# MQTT Конфигурация
broker = "109.104.195.26"
username = "trafficcontrol"
password = "parolata1"

# Информация за датабазата
DB_HOST = "localhost"
DB_USER = "stc"
DB_PASS = "stc_pass"
DB_NAME = "stc"
normalmode = True

numbers = set()
numbersop = set()
numbersaf = set()
seconds = 0

def get_db_connection():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

def setup_mqtt():
    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.on_message = on_message
    client.connect(broker, 1883, 60)
    topics = ["numbers/detect2", "numbers/detect3", "numbers/detect6"]
    for topic in topics:
        client.subscribe(topic)
        print(f"📡 Засичане на номера '{topic}'")
    return client

def on_message(client, userdata, message):
    global numbers
    global numbersop
    global numbersaf
    received_number = message.payload.decode().strip()
    received_topic = message.topic
    if received_topic == "numbers/detect2":
        if received_number not in numbersop:
            numbersop.add(received_number)
            print(f"🚗 Засечен номер: {received_number} от топик: {received_topic}")
            global seconds
            seconds+=6
            print(seconds)
            print(numbersop)
            conn = get_db_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT valid_vignette, valid_insurance	 
                        FROM cmsapp_vehicles 
                        WHERE A=%s
                    """, (received_number.strip(),))
                    result = cursor.fetchone()
                    
                    if result:
                        if result['valid_vignette'] == 0:
                            print("Колата няма винетка, изпраща се сигнал до най-близкия патрул.")
                        if result['valid_insurance'] == 0:
                            print("Колата няма застраховка, изпраща се сигнал до най-близкия патрул.")

                    else:
                        print("ℹ️ Няма данни за този номер в базата.")
            finally:
                conn.close()
        else:   
            print(f"⚠️ Номерът {received_number} вече е засечен.")
    elif received_topic == "numbers/detect3":
        if received_number not in numbers:
            numbers.add(received_number)
            print(f"🚗 Засечен номер: {received_number} от топик: {received_topic}")
            print(numbers)
            conn = get_db_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT valid_vignette, valid_insurance	 
                        FROM cmsapp_vehicles 
                        WHERE A=%s
                    """, (received_number.strip(),))
                    result = cursor.fetchone()
                    
                    if result:
                        if result['valid_vignette'] == 0:
                            print("Колата няма винетка, изпраща се сигнал до най-близкия патрул.")
                        if result['valid_insurance'] == 0:
                            print("Колата няма застраховка, изпраща се сигнал до най-близкия патрул.")

                    else:
                        print("ℹ️ Няма данни за този номер в базата.")
            finally:
                conn.close()
        else:   
            print(f"⚠️ Номерът {received_number} вече е засечен.")
    elif received_topic == "numbers/detect6":
        if received_number not in numbersaf:
            numbersaf.add(received_number)
            print(f"🚗 Засечен номер: {received_number} от топик: {received_topic}")
            print(numbersaf)
            conn = get_db_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT valid_vignette, valid_insurance	 
                        FROM cmsapp_vehicles 
                        WHERE A=%s
                    """, (received_number.strip(),))
                    result = cursor.fetchone()
                    
                    if result:
                        if result['valid_vignette'] == 0:
                            print("Колата няма винетка, изпраща се сигнал до най-близкия патрул.")
                        if result['valid_insurance'] == 0:
                            print("Колата няма застраховка, изпраща се сигнал до най-близкия патрул.")

                    else:
                        print("ℹ️ Няма данни за този номер в базата.")
            finally:
                conn.close()
        else:   
            print(f"⚠️ Номерът {received_number} вече е засечен.")

def execute_commands(commands):
    processes = [subprocess.Popen(cmd, shell=True) for cmd in commands]
    for process in processes:
        process.wait()

# Извлича данните за светофарите
conn = get_db_connection()
cursor = conn.cursor()
sqlt = "SELECT * FROM cmsapp_traffic_lights"
cursor.execute(sqlt)
trafficlight = cursor.fetchall()

# MQQT Команди
firsttrafficlights = [
    f"mosquitto_pub -h {broker} -t {row['topic']} -m {'red' if row['topic'] in ['traffic/light2', 'traffic/light3'] else 'green'} -u {username} -P {password}"
    for row in trafficlight
]

secondtrafficlights = [
f"mosquitto_pub -h {broker} -t {row['topic']} -m {'green' if row['topic'] in ['traffic/light2', 'traffic/light3'] else ('bothred' if row['topic'] in ['traffic/light1', 'traffic/light4'] else 'red')} -u {username} -P {password}"
    for row in trafficlight
]

thirdtrafficlights = [
    f"mosquitto_pub -h {broker} -t {row['topic']} -m {'green' if row['topic'] in ['traffic/light2', 'traffic/light3'] else 'red'} -u {username} -P {password}"
    for row in trafficlight
]

# Функция за autocontrollera
def traffic_light_loop():
    global seconds
    while True:
        if seconds == 0:
            seconds = 20
            
        execute_commands(firsttrafficlights)
        time.sleep(seconds)
        execute_commands(secondtrafficlights)
        time.sleep(20)
        execute_commands(thirdtrafficlights)
        time.sleep(seconds)


# Loop
if __name__ == "__main__":
    traffic_thread = threading.Thread(target=traffic_light_loop, daemon=True)
    traffic_thread.start()
    client = setup_mqtt()
    client.loop_forever()

cursor.close()
conn.close()
