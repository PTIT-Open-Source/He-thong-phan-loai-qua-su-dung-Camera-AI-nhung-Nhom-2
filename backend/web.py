import os
import ssl
from flask import Flask, render_template, send_from_directory
import paho.mqtt.client as mqtt

app = Flask(__name__, template_folder='.')
UPLOAD_FOLDER = "/home/hedieuhanh/excel"
DETECTION_FOLDER = "/home/hedieuhanh/detection_log"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DETECTION_FOLDER, exist_ok=True)

# Thong tin MQTT HiveMQ Cloud
MQTT_BROKER = "978cc58167af4b0c99c7739f7d327252.s1.eu.hivemq.cloud"
MQTT_PORT = 8883  # Dung TLS cong 8883
MQTT_TOPIC = "excel/upload"
MQTT_USERNAME = "ducmanh97"  
MQTT_PASSWORD = "Ducmanh97"  

# Callback khi nhan tin nhan MQTT
def on_message(client, userdata, message):
    parts = message.topic.split("/")
    filename = parts[-1] if len(parts) >= 3 else "received_file.xlsx"
    folder = DETECTION_FOLDER if "detection_log" in filename else UPLOAD_FOLDER
    filepath = os.path.join(folder, filename)
    
    with open(filepath, "wb") as f:
        f.write(message.payload)
    
    print(f"Received and saved: {filename} in {folder}")

# Ham khi ket noi MQTT thanh cong
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to HiveMQ Cloud successfully!")
        client.subscribe(MQTT_TOPIC + "/#")  # Lang nghe tat ca cac file Excel tai len
    else:
        print(f"Connection failed with error code {rc}")

# Cau hinh MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)  # Dang nhap
mqtt_client.tls_set(cert_reqs=ssl.CERT_NONE)  # Kich hoat TLS 
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Ket noi HiveMQ Cloud
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

@app.route("/")
def index():
    excel_files = sorted(os.listdir(UPLOAD_FOLDER), reverse=True)
    detection_files = sorted(os.listdir(DETECTION_FOLDER), reverse=True)
    return render_template("index.html", excel_files=excel_files, detection_files=detection_files)

@app.route("/download/<folder>/<filename>")
def download(folder, filename):
    if folder == "excel":
        directory = UPLOAD_FOLDER
    elif folder == "detection":
        directory = DETECTION_FOLDER
    else:
        return "Invalid folder", 404
    return send_from_directory(directory, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
