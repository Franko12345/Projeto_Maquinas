import cv2
import time

import RPi.GPIO as GPIO
import serial

# Configuração UART
UART_PORT = "/dev/ttyS0"  # Pode ser /dev/ttyS0 dependendo da config
BAUD_RATE = 9600

serial_port = serial.Serial(port=UART_PORT, baudrate=BAUD_RATE, timeout=1)

# Configuração GPIO
GPIO.setmode(GPIO.BCM)
LED_PIN = 18
GPIO.setup(LED_PIN, GPIO.OUT)



face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Camera nao disponivel")

else:
    width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"res: {width}x{height}")

input()

def detect_bounding_box(vid):
    global width, height
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))

    if len(faces) == 0:
        return 0

    face = max(faces, key=lambda x: x[2]*x[3])
    (x, y, w, h) = face

    return (int(round((x+w/2)-round(width/2))), int(round((y+h/2)-round(height/2))))

delay = True

while True:
    st = time.time()

    result, video_frame = video_capture.read()

    if result is False:
        break

    face = detect_bounding_box(video_frame)

    if(face != 0):
        payload = f"{face[0]},{face[1]}\n"
    else:
        payload = "null\n"

    serial_port.write(payload.encode("utf-8"))
    # print(f"[TX] Enviado: {payload}")

    if delay:
        ellapsed_time = time.time()-st
        # print(f"Ellapsed time {ellapsed_time}")
        time.sleep(max(0, 0.1-ellapsed_time)) # desafogar serial

video_capture.release()
cv2.destroyAllWindows()
