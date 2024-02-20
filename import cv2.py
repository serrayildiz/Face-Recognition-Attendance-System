import cv2
import requests
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
camera_url = 'http://172.19.40.104:8080/video'  # IP kameranın video URL'si
stream = requests.get(camera_url, stream=True)

if stream.status_code == 200:
    bytes = bytes()
    for chunk in stream.iter_content(chunk_size=1024):
        bytes += chunk
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

            # Yüzleri bulma
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Bulunan yüzleri dikdörtgen içine alın ve görüntüyü gösterin
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            cv2.imshow('IP Kamera Akışı', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
else:
    print("Video akışına bağlanılamadı.")

cv2.destroyAllWindows()
