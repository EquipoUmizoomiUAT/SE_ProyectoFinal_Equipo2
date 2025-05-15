import serial
import time
import requests
from ILS import runILS
from GlobalConfig import GetGlobalConfig

PORT = 'COM3'
BAUD_RATE = 9600
API_URL = "http://localhost:3000/api/v1/records"

# Orden de potencia de los relevadores (más luz a menos luz)
relevadores_por_potencia = [3, 2, 1]

# Estado actual de los relevadores (todos empiezan apagados)
estado = {1: False, 2: False, 3: False}

config = GetGlobalConfig()


def enviar_registro(id_device, current_value):
    data = {
        "id_device": str(id_device),
        "current_value": str(current_value)
    }
    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 201:
            print(f"Registro enviado: Dispositivo {id_device}, Valor {current_value}")
        else:
            print(f"Error al enviar registro: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con la API: {e}")


def leer_ldr(ser):
    """Lee el valor de intensidad del LDR desde el serial"""
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("IntL:"):
            try:
                valor = int(line.split(":")[1].strip())
                print(f"Intensidad actual (VA): {valor}")
                # Enviamos el valor del LDR a la API (id_device: 1)
                enviar_registro(1, valor)
                return valor
            except ValueError:
                continue


def invertir_relevador(ser, r):
    """Envía el número del relevador para invertir su estado"""
    ser.write(str(r).encode('utf-8'))
    estado[r] = not estado[r]
    estado_num = 1 if estado[r] else 0
    print(f"{'Encendido' if estado[r] else 'Apagado'} relevador {r}")

    # Enviamos el estado del relevador a la API (id_device: r+1)
    enviar_registro(r + 1, estado_num)
    time.sleep(1)


def ajustar_relevadores(ser):
    VA = leer_ldr(ser)  # Esta función ahora ya envía el registro del LDR
    VO = runILS(VA)
    print(f"Valor óptimo (VO): {VO}")

    if VO > VA:
        # Necesitamos más luz → prender el más potente que esté apagado
        for r in relevadores_por_potencia:
            if not estado[r]:
                print(f"Encendiendo relevador {r} para aumentar luz")
                invertir_relevador(ser, r)  # Esta función envía el registro del relevador
                break
    elif VO < VA:
        # Necesitamos menos luz → apagar el más potente que esté encendido
        for r in relevadores_por_potencia:
            if estado[r]:
                print(f"Apagando relevador {r} para reducir luz")
                invertir_relevador(ser, r)  # Esta función envía el registro del relevador
                break
    else:
        print("Intensidad adecuada, sin cambios.")


def main():
    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        print("Conectado al Arduino.")

        while True:
            ajustar_relevadores(ser)
            print("⏱ Esperando 1 segundo...\n")
            time.sleep(1)

    except serial.SerialException as e:
        print("Error con el puerto serial:", e)
    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Puerto serial cerrado.")


if __name__ == "__main__":
    main()