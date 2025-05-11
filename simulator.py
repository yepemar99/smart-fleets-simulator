import pika
import json
import time
import random

# RabbitMQ config
RABBITMQ_HOST = 'localhost'
RABBITMQ_QUEUE = 'InputMessages'
RABBITMQ_USER = 'guest'
RABBITMQ_PASS = 'guest'

# Conexión
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

# IDs permitidos por tipo
COMBUSTION_IDS = [4]
ELECTRIC_IDS = []
HYBRID_IDS = []

def random_coords():
    return round(random.uniform(-90, 90), 6), round(random.uniform(-180, 180), 6)

def generate_combustion_vehicle_data():
    if not COMBUSTION_IDS:
        return None
    lat, lon = random_coords()
    return {
        "id": random.choice(COMBUSTION_IDS),
        "timestamp": int(time.time() * 1000),
        "latitude": lat,
        "longitude": lon,
        "temperature": round(random.uniform(30, 110), 2),
        "speed": round(random.uniform(0, 180), 2),
        "oilPressure": round(random.uniform(5, 80), 2),
        "oilLevel": round(random.uniform(1, 100), 2),
        "rpm": random.randint(800, 5000),
        "fuelMixture": round(random.uniform(12.0, 15.5), 2),
        "gasEmissions": round(random.uniform(0.1, 1.5), 2),
        "coolantTemperature": round(random.uniform(70, 125), 2),
        "alternatorVoltage": round(random.uniform(7.0, 14.8), 2),
        "doorStatus": random.choice([0.0, 1.0]),
        "eventTypeName": "CombustionVehicle"
    }

def generate_electric_vehicle_data():
    if not ELECTRIC_IDS:
        return None
    lat, lon = random_coords()
    return {
        "id": random.choice(ELECTRIC_IDS),
        "timestamp": int(time.time() * 1000),
        "latitude": lat,
        "longitude": lon,
        "speed": round(random.uniform(0, 160), 2),
        "batteryLevel": round(random.uniform(5, 100), 2),
        "batteryTemperature": round(random.uniform(20, 100), 2),
        "chargingStatus": random.choice([True, False]),
        "cargoDoorStatus": random.choice([True, False]),
        "shockSensor": random.choice([True, False]),
        "motorStatus": random.choice([True, False]),
        "eventTypeName": "ElectricVehicle"
    }

def generate_hybrid_vehicle_data():
    if not HYBRID_IDS:
        return None
    lat, lon = random_coords()
    return {
        "id": random.choice(HYBRID_IDS),
        "timestamp": int(time.time() * 1000),
        "latitude": lat,
        "longitude": lon,
        "speed": round(random.uniform(0, 180), 2),
        "engineTemperature": round(random.uniform(70, 110), 2),
        "fuelLevel": round(random.uniform(5, 100), 2),
        "batteryCharge": round(random.uniform(10, 100), 2),
        "fuelEfficiency": round(random.uniform(10, 25), 2),
        "rpm": random.randint(800, 4500),
        "batteryTemperature": round(random.uniform(20, 105), 2),
        "batteryVoltage": round(random.uniform(100, 400), 2),
        "batteryCurrent": round(random.uniform(0, 50), 2),
        "regenEfficiency": round(random.uniform(20, 95), 2),
        "eventTypeName": "HybridVehicle"
    }

# Simulación
simulation_duration = 180  # segundos
start_time = time.time()

# Lista de generadores activos
generators = []

if COMBUSTION_IDS:
    generators.append(generate_combustion_vehicle_data)
if ELECTRIC_IDS:
    generators.append(generate_electric_vehicle_data)
if HYBRID_IDS:
    generators.append(generate_hybrid_vehicle_data)

if not generators:
    print("No hay tipos de vehículos habilitados para la simulación. Verifica los arreglos de IDs.")
else:
    while (time.time() - start_time) < simulation_duration:
        generator = random.choice(generators)
        data = generator()
        if data:
            message = json.dumps(data)
            channel.basic_publish(
                exchange='',
                routing_key=RABBITMQ_QUEUE,
                body=message,
                properties=pika.BasicProperties(delivery_mode=2)
            )
            print(data)
            print(f"[x] Enviado: {data['eventTypeName']} - {data['id']}")
        time.sleep(3)

    connection.close()
    print("Simulación terminada.")
