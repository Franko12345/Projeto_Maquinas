from machine import UART, Pin, PWM
import time

# Configuração do pino (ex: D4 no NodeMCU = GPIO2)
servo = PWM(Pin(14), freq=50)  # 50 Hz → 20 ms de período

# Função para mover o servo em um ângulo específico (0° a 180°)
def set_angle(angle):
    min_duty = 40     # ~0.5 ms	
    max_duty = 115    # ~2.5 ms
    duty = int(min_duty + (angle / 140) * (max_duty - min_duty))
    servo.duty(duty)

# Configuração da UART2 do ESP32
uart = UART(2, baudrate=9600, tx=17, rx=16)

# LED de teste (pino interno da maioria das placas ESP32)
led = Pin(2, Pin.OUT)
led.value(0)  # LED desligado (depende da placa)

print("UART ESP32 iniciada em TX=GPIO17, RX=GPIO16")

angle = 70

def clamp(a, ma, mi):
    return min(max(a, mi), ma)

while True:
    # Verifica se há dados recebidos
    if uart.any():
        data = uart.readline()

        if data:
            msg = data.decode("utf-8").strip()
            print("📩 Recebido:", msg)

            if msg.lower() == "null":
                pass
            else:
                x, y = map(int, msg.split(","))
                print(f"X:{x}, Y:{y}")
                angle = clamp(angle+x/50 , 0, 140)
    set_angle(angle)
                
