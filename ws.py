import websocket
import json
import threading
import serial

def on_message(ws, message):
    message_json = json.loads(message)
    data = json.loads(message_json['data'])
    led_status = data['message']
    print("Enviando:", led_status)

    # Conexión serial
    with serial.Serial('COM5', 115200) as ser:
        # Enviar datos al Arduino a través de la conexión serial
        if led_status:
            print("Enviando '1' al Arduino")
            val = b'1'
            ser.write(val)
        else:
            print("No se envía nada al Arduino")

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send(json.dumps({
        'event': 'pusher:subscribe',
        'data': {
            'channel': 'servo'
        }
    }))

if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://192.168.1.11:6001/app/goodfonyerv",
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
