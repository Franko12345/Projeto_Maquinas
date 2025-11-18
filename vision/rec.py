import cv2
import time

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

video_capture = cv2.VideoCapture(2)

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

    cv2.circle(vid, (int(x+w/2), int(y+h/2)), 5, (0, 255, 0), 4)
    cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
    cv2.putText(vid, f"X: {int(round((x+w/2)-round(width/2)))} Y:{int(round((y+h/2)-round(height/2)))}", (x, y), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255))

    return (x+w/2, y+h/2)

delay = True

while True:
    st = time.time()

    result, video_frame = video_capture.read()

    if result is False:
        break

    faces = detect_bounding_box(video_frame)

    cv2.imshow("My Face Detection Project", video_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    if delay:
        ellapsed_time = time.time()-st
        print(f"Ellapsed time {ellapsed_time}")
        time.sleep(max(0, 0.05-ellapsed_time)) # desafogar serial

video_capture.release()
cv2.destroyAllWindows()
