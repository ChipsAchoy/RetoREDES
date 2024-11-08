import requests
import time
import logging
from plyer import notification

# Credenciales e IDs
API_KEY = 'f6da1a72fe22257d79966bfbfd2bd73adc11f34c'
NETWORK_ID = 'L_646829496481105433'

# Headers de autenticación
headers = {
    'X-Cisco-Meraki-API-Key': API_KEY,
    'Content-Type': 'application/json'
}

# Lista de seriales de tus dispositivos para consultar su estado
device_serials = ['Q2QN-9J8L-SLPD', 'Q2MD-BHHS-5FDL', 'Q2HP-F5K5-R88R']
initial_device_serials = device_serials.copy()  # Guardamos la lista inicial

# Configuración del logger
logging.basicConfig(filename="cambios_dispositivos.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(message)s")

# Función para monitorear cada dispositivo
def monitor_dispositivos():
    for serial in device_serials:
        url = f'https://api.meraki.com/api/v1/devices/{serial}'
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            device_info = response.json()
            print(f"\nDispositivo: {device_info.get('model')}")
            print(f"  IP LAN: {device_info.get('lanIp', 'No disponible')}")
            print(f"  Firmware: {device_info.get('firmware', 'No disponible')}")
            print(f"  Última actualización de configuración: {device_info.get('configurationUpdatedAt', 'No disponible')}")
        else:
            print(f"Error al obtener la información del dispositivo {serial}: {response.status_code}")

# Función para notificación de cambios en el escritorio
def notificacion_escritorio(mensaje):
    notification.notify(
        title="Alerta de Monitoreo de Dispositivos",
        message=mensaje,
        app_name="Monitor de Dispositivos",
        timeout=10  # duración de la notificación en segundos
    )

# Ejecutar monitoreo una vez cada minuto
while True:
    monitor_dispositivos()

    # Verificar si la lista de dispositivos ha cambiado
    if device_serials != initial_device_serials:
        mensaje_cambio = "La lista de dispositivos ha cambiado."
        logging.info(mensaje_cambio)
        notificacion_escritorio(mensaje_cambio)
        initial_device_serials = device_serials.copy()  # Actualizamos la lista inicial
    
    # Preguntar si se desea agregar o quitar un dispositivo
    print("\n¿Deseas agregar o quitar un dispositivo?")
    action = input("Escribe 'agregar' para añadir un dispositivo, 'quitar' para eliminar uno, o 'no' para continuar: ").strip().lower()
    
    if action == 'agregar':
        serial = input("Ingresa el serial del dispositivo a agregar: ").strip()
        if serial not in device_serials:
            device_serials.append(serial)
            print(f"Dispositivo {serial} agregado.")
            logging.info(f"Dispositivo {serial} agregado.")
        else:
            print("El dispositivo ya está en la lista.")
    
    elif action == 'quitar':
        serial = input("Ingresa el serial del dispositivo a quitar: ").strip()
        if serial in device_serials:
            device_serials.remove(serial)
            print(f"Dispositivo {serial} eliminado.")
            logging.info(f"Dispositivo {serial} eliminado.")
        else:
            print("El dispositivo no está en la lista.")
    
    print("\nEsperando 30 segundos para la próxima verificación...\n")
    time.sleep(30)
