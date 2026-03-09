from machine import Pin, ADC
import network
import time
import dht
from umqtt.simple import MQTTClient
import json

# =============================
# WIFI SETTINGS
# =============================
SSID = "RumahAlpha-2.4G@unifi"
PASSWORD = "204rumahalpha"

# =============================
# MQTT SETTINGS
# =============================
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC_DATA = b"smart_irrigation/data"
MQTT_TOPIC_CONTROL = b"smart_irrigation/control"
CLIENT_ID = "esp32-irrigation-001"

# =============================
# RELAYS
# =============================
pump1 = Pin(25, Pin.OUT)
pump2 = Pin(26, Pin.OUT)
sol1  = Pin(27, Pin.OUT)
sol2  = Pin(14, Pin.OUT)

def pump_sol_on(pump, sol):
    pump.value(1)
    sol.value(1)

def pump_sol_off(pump, sol):
    pump.value(0)
    sol.value(0)

pump_sol_off(pump1, sol1)
pump_sol_off(pump2, sol2)

# =============================
# SENSORS
# =============================
soil1 = ADC(Pin(34))
soil2 = ADC(Pin(35))
soil1.atten(ADC.ATTN_11DB)
soil2.atten(ADC.ATTN_11DB)

dht_sensor = dht.DHT22(Pin(15))

# =============================
# SETTINGS
# =============================
SOIL_DRY = 2500
SOIL_MOIST = 2100
MAX_WATERING = 30
PUBLISH_INTERVAL = 10

# =============================
# STATE
# =============================
watering_state = {
    "pump1": False,
    "pump2": False,
    "sol1": False,
    "sol2": False,
    "start_time1": None,
    "start_time2": None
}

# =============================
# WIFI CONNECT
# =============================
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
def connect_wifi():
    if not wifi.isconnected():
        print("Connecting WiFi...")
        wifi.connect(SSID, PASSWORD)
        t = 20
        while not wifi.isconnected() and t>0:
            print(".", end="")
            time.sleep(1)
            t -= 1
        print("\nWiFi connected" if wifi.isconnected() else "\nWiFi failed")
connect_wifi()

# =============================
# MQTT CONNECT
# =============================
def mqtt_callback(topic, msg):
    try:
        cmd = json.loads(msg)
        # Manual override
        if 'pump1' in cmd:
            if cmd['pump1']: pump_sol_on(pump1, sol1)
            else: pump_sol_off(pump1, sol1)
            watering_state["pump1"] = cmd['pump1']
            watering_state["sol1"] = cmd['sol1']
        if 'pump2' in cmd:
            if cmd['pump2']: pump_sol_on(pump2, sol2)
            else: pump_sol_off(pump2, sol2)
            watering_state["pump2"] = cmd['pump2']
            watering_state["sol2"] = cmd['sol2']
    except Exception as e:
        print("MQTT control error:", e)

client = MQTTClient(CLIENT_ID, MQTT_BROKER, keepalive=60)
client.set_callback(mqtt_callback)
client.connect()
client.subscribe(MQTT_TOPIC_CONTROL)
print("MQTT connected and subscribed")

# =============================
# AUTO-WATERING LOGIC
# =============================
def apply_watering():
    s1 = soil1.read()
    s2 = soil2.read()
    now = time.time()

    # Pump1
    if s1 > SOIL_DRY:
        if not watering_state["pump1"]:
            watering_state["start_time1"] = now
            print("Pump1 START (soil dry)")
        pump_sol_on(pump1, sol1)
        watering_state["pump1"] = True
        watering_state["sol1"] = True
    elif s1 <= SOIL_MOIST:
        pump_sol_off(pump1, sol1)
        watering_state["pump1"] = False
        watering_state["sol1"] = False
        watering_state["start_time1"] = None

    # Pump2
    if s2 > SOIL_DRY:
        if not watering_state["pump2"]:
            watering_state["start_time2"] = now
            print("Pump2 START (soil dry)")
        pump_sol_on(pump2, sol2)
        watering_state["pump2"] = True
        watering_state["sol2"] = True
    elif s2 <= SOIL_MOIST:
        pump_sol_off(pump2, sol2)
        watering_state["pump2"] = False
        watering_state["sol2"] = False
        watering_state["start_time2"] = None

    # Max watering check
    if watering_state["start_time1"] and watering_state["pump1"]:
        if now - watering_state["start_time1"] > MAX_WATERING:
            print("Pump1 max watering reached")
            pump_sol_off(pump1, sol1)
            watering_state["pump1"] = False
            watering_state["sol1"] = False
            watering_state["start_time1"] = None

    if watering_state["start_time2"] and watering_state["pump2"]:
        if now - watering_state["start_time2"] > MAX_WATERING:
            print("Pump2 max watering reached")
            pump_sol_off(pump2, sol2)
            watering_state["pump2"] = False
            watering_state["sol2"] = False
            watering_state["start_time2"] = None

# =============================
# MAIN LOOP
# =============================
while True:
    try:
        client.check_msg()  # Manual MQTT commands

        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        s1 = soil1.read()
        s2 = soil2.read()

        apply_watering()

        payload = {
            "soil1": s1,
            "soil2": s2,
            "temperature": temp,
            "humidity": hum,
            "pump1": watering_state["pump1"],
            "pump2": watering_state["pump2"],
            "sol1": watering_state["sol1"],
            "sol2": watering_state["sol2"],
            "timestamp": time.time()
        }
        client.publish(MQTT_TOPIC_DATA, json.dumps(payload))
        print("Sent:", payload)

        time.sleep(PUBLISH_INTERVAL)
    except Exception as e:
        print("Error:", e)
        time.sleep(5)
