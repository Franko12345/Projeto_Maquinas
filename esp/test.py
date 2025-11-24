from machine import UART, Pin, PWM
from time import sleep

# Configuração do pino (ex: D4 no NodeMCU = GPIO2)
servo = PWM(Pin(14), freq=50)  # 50 Hz → 20 ms de período

# Função para mover o servo em um ângulo específico (0° a 180°)
def set_angle(angle):
    min_duty = 40     # ~0.5 ms	
    max_duty = 115    # ~2.5 ms
    duty = int(min_duty + (angle / 140) * (max_duty - min_duty))
    servo.duty(duty)
    
while True:
    set_angle(0)
    print("Ângulo: 0°")
    sleep(1)
    set_angle(70)
    print("Ângulo: 70°")
    sleep(1)
    set_angle(140)
    print("Ângulo: 140°")
    sleep(1)
